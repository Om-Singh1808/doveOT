import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
  saveFile: (filters: Electron.FileFilter[], defaultName: string) =>
    ipcRenderer.invoke('dialog:saveFile', filters, defaultName),

  openExternal: (url: string) =>
    ipcRenderer.invoke('shell:openExternal', url),

  minimize: () => ipcRenderer.invoke('app:minimize'),
  maximize: () => ipcRenderer.invoke('app:maximize'),
  close: () => ipcRenderer.invoke('app:close'),
})
