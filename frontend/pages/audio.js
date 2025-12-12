
import { useState, useRef } from 'react';

export default function AudioPage(){
  const [status,setStatus]=useState('idle');
  const mediaRecorder = useRef(null);
  const audioChunks = useRef([]);
  async function startRec(){
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder.current = new MediaRecorder(stream);
    mediaRecorder.current.ondataavailable = e => audioChunks.current.push(e.data);
    mediaRecorder.current.onstop = upload;
    audioChunks.current = [];
    mediaRecorder.current.start();
    setStatus('recording');
  }
  function stopRec(){
    mediaRecorder.current.stop();
    setStatus('stopped');
  }
  async function upload(){
    const blob = new Blob(audioChunks.current, { type: 'audio/webm' });
    const fd = new FormData();
    fd.append('file', blob, 'recording.webm');
    fd.append('speaker', 'web_user');
    const res = await fetch('http://localhost:8000/api/upload-audio', { method: 'POST', body: fd });
    const j = await res.json();
    setStatus(JSON.stringify(j));
  }
  return (
    <main style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Upload audio</h1>
      <p>Status: {status}</p>
      <button onClick={startRec}>Start</button>
      <button onClick={stopRec}>Stop</button>
    </main>
  )
}
