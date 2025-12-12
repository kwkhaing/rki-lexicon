
import { useState } from 'react';

export default function Home(){
  const [q,setQ]=useState('');
  const [results,setResults]=useState(null);
  async function doSearch(){
    const res = await fetch(`http://localhost:8000/api/search?q=${encodeURIComponent(q)}`);
    const j = await res.json();
    setResults(j.results);
  }
  return (
    <main style={{padding:20,fontFamily:'sans-serif'}}>
      <h1>Rakhine (rki) Lexicon</h1>
      <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search word or gloss" />
      <button onClick={doSearch}>Search</button>
      <div>
        {results && results.map((r,i)=>(
          <div key={i} style={{border:'1px solid #ddd',margin:8,padding:8}}>
            <h3>{r.word}</h3>
            <div>{r.definitions.map((d,idx)=>(<div key={idx}><strong>{d.gloss}</strong> — {d.english}</div>))}</div>
          </div>
        ))}
      </div>
      <p><a href="/submit">Submit a word</a> • <a href="/audio">Upload audio</a></p>
    </main>
  )
}
