// Prevents additional console window on Windows in release, DO NOT REMOVE!!
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::Manager;
use tauri_plugin_shell::ShellExt;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .plugin(tauri_plugin_log::Builder::default()
      .level(log::LevelFilter::Info)
      .format(|out, message, record| {
        out.finish(format_args!("[{}] {}: {}", chrono::Local::now().format("%Y-%m-%d %H:%M:%S"), record.level(), message))
      })
      .build())
    .plugin(tauri_plugin_shell::init())
    .plugin(tauri_plugin_opener::init())
    .plugin(tauri_plugin_process::init())
    .plugin(tauri_plugin_fs::init())
    .setup(|app| {
      // Start Python backend sidecar in release mode
      #[cfg(not(debug_assertions))]
      {
        let handle = app.handle().clone();
        tauri::async_runtime::spawn(async move {
          if let Err(e) = start_python_backend(handle).await {
            log::error!("Failed to start Python backend: {}", e);
          }
        });
      }
      Ok(())
    })
    .invoke_handler(tauri::generate_handler![
      get_python_backend_status,
      get_app_version
    ])
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}

async fn start_python_backend(handle: tauri::AppHandle) -> Result<(), Box<dyn std::error::Error>> {
  let shell = handle.shell();
  let command = shell.sidecar("vedic-ai-backend")?;
  
  let (mut rx, _child) = command.spawn()?;
  
  // Monitor the sidecar process
  tauri::async_runtime::spawn(async move {
    while let Some(event) = rx.recv().await {
      match event {
        tauri_plugin_shell::process::CommandEvent::Stdout(line) => {
          log::info!("[Python Backend] {}", String::from_utf8_lossy(&line));
        }
        tauri_plugin_shell::process::CommandEvent::Stderr(line) => {
          log::error!("[Python Backend] {}", String::from_utf8_lossy(&line));
        }
        tauri_plugin_shell::process::CommandEvent::Error(e) => {
          log::error!("[Python Backend] Error: {}", e);
        }
        tauri_plugin_shell::process::CommandEvent::Terminated(payload) => {
          log::warn!("[Python Backend] Terminated with code: {:?}", payload.code);
        }
        _ => {}
      }
    }
  });
  
  Ok(())
}

#[tauri::command]
async fn get_python_backend_status() -> Result<String, String> {
  // Check if backend is reachable
  let client = reqwest::Client::new();
  match client.get("http://127.0.0.1:8000/api/v1/health")
    .timeout(std::time::Duration::from_secs(2))
    .send()
    .await
  {
    Ok(response) if response.status().is_success() => Ok("running".to_string()),
    Ok(_) => Ok("unhealthy".to_string()),
    Err(_) => Ok("stopped".to_string()),
  }
}

#[tauri::command]
async fn get_app_version() -> String {
  env!("CARGO_PKG_VERSION").to_string()
}