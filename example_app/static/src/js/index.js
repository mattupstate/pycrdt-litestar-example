import * as Y from 'yjs'
import { WebsocketProvider } from 'y-websocket'
import CodeMirror from 'codemirror'
import { CodemirrorBinding } from 'y-codemirror'
import 'codemirror/mode/javascript/javascript.js'
import '../css/codemirror.css'

const ydoc = new Y.Doc()
const provider = new WebsocketProvider('ws://localhost:8000/ws', 'hello', ydoc)
const yText = ydoc.getText('codemirror')

const editorContainer = document.querySelector('#editor')

window.myEditor = CodeMirror(editorContainer, {
    mode: 'python',
    lineNumbers: true
})

const binding = new CodemirrorBinding(yText, window.myEditor, provider.awareness)
