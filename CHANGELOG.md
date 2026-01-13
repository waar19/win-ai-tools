# Changelog

Todos los cambios notables de este proyecto se documentan aquí.

## [v1.0.0] - 2026-01-13

### 🎉 Release Inicial

#### Características

- ✨ Interfaz gráfica moderna con tema oscuro (PyQt6)
- 🤖 Detección de 11 servicios AI de Windows 11:
  - Microsoft Copilot
  - Windows Recall
  - AI Explorer
  - Bing Search en Start Menu
  - Web Search en Taskbar
  - Windows Widgets (AI News)
  - Cortana (Legacy)
  - Edge Copilot Sidebar
  - AI Voice Typing
  - Suggested Actions
- ⚡ Habilitar/Deshabilitar servicios individualmente
- 🚫 Botón para deshabilitar todos los servicios
- 💾 Sistema de backup antes de modificar
- ↩️ Restauración desde backups
- 📋 Log de actividad con historial persistente
- 🛡️ Solicitud automática de permisos de administrador

#### Técnico

- Ejecutable standalone (.exe) - No requiere Python instalado
- Modificación de Registry para desactivar servicios
- Remoción de paquetes Appx cuando aplica
- Icono personalizado de la aplicación
