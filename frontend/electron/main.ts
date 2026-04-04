import { app, BrowserWindow, ipcMain, dialog, shell } from 'electron'
import path from 'path'
import url from 'url'
import { spawn, ChildProcess } from 'child_process'

const __filename = url.fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

let mainWindow: BrowserWindow | null = null
let pythonProcess: ChildProcess | null = null

const isDev = process.env.NODE_ENV === 'development'

function startPythonBackend() {
  const backendPath = isDev
    ? path.join(__dirname, '..', '..', 'backend')
    : path.join(process.resourcesPath, 'backend')

  const pythonExec = process.platform === 'win32' ? 'python' : 'python3'

  pythonProcess = spawn(pythonExec, ['main.py'], {
    cwd: backendPath,
    env: { ...process.env },
    stdio: ['ignore', 'pipe', 'pipe'],
  })

  pythonProcess.stdout?.on('data', (data) => {
    console.log(`[Backend] ${data.toString().trim()}`)
  })

  pythonProcess.stderr?.on('data', (data) => {
    console.error(`[Backend ERR] ${data.toString().trim()}`)
  })

  pythonProcess.on('close', (code) => {
    console.log(`[Backend] exited with code ${code}`)
  })
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1024,
    minHeight: 700,
    backgroundColor: '#0a0a0f',
    titleBarStyle: 'hiddenInset',
    frame: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false,
    },
  })

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173')
    mainWindow.webContents.openDevTools()
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'))
  }

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

// --- IPC Handlers ---

ipcMain.handle('dialog:saveFile', async (_, filters: Electron.FileFilter[], defaultName: string) => {
  if (!mainWindow) return null
  const result = await dialog.showSaveDialog(mainWindow, {
    defaultPath: defaultName,
    filters,
  })
  return result.filePath ?? null
})

ipcMain.handle('shell:openExternal', (_, url: string) => {
  shell.openExternal(url)
})

ipcMain.handle('app:minimize', () => mainWindow?.minimize())
ipcMain.handle('app:maximize', () => {
  if (mainWindow?.isMaximized()) {
    mainWindow.unmaximize()
  } else {
    mainWindow?.maximize()
  }
})
ipcMain.handle('app:close', () => mainWindow?.close())

// --- App lifecycle ---

app.whenReady().then(() => {
  startPythonBackend()
  createWindow()
})

app.on('window-all-closed', () => {
  if (pythonProcess) {
    pythonProcess.kill()
  }
  if (process.platform !== 'darwin') app.quit()
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) createWindow()
})
