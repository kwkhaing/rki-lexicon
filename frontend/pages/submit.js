
import { useState } from 'react';

export default function Submit(){
  const [entry,setEntry]=useState('');
  const [msg,setMsg]=useState('');
  async function submit(){
    const form = new FormData();
    form.append('entry', entry);
    const res = await fetch('http://localhost:8000/api/submit', { method: 'POST', body: form });
    const j = await res.json();
    setMsg(JSON.stringify(j));
  }
  return (
    <main style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Submit a word or entry</h1>
      <textarea value={entry} onChange={e=>setEntry(e.target.value)} rows={12} cols={80} placeholder='Paste JSON here'></textarea>
      <div>
        <button onClick={submit}>Submit</button>
      </div>
      <pre>{msg}</pre>
    </main>
  )
}
