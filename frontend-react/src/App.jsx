import { useState, useEffect } from 'react'
import axios from 'axios'

function App() {
  const [vagas, setVagas] = useState([])
  const [novoTermo, setNovoTermo] = useState('')
  const [loading, setLoading] = useState(true)
  const [processando, setProcessando] = useState(false)

  // --- O FILTRO VIP DE TEXTOS ---
  const formatarTitulo = (texto) => {
    if (!texto) return '';
    let limpo = texto;
    limpo = limpo.replace(/([a-z])([A-Z])/g, '$1 $2');
    limpo = limpo.replace(/Analistade/gi, 'Analista de ');
    limpo = limpo.replace(/Pessoade/gi, 'Pessoa de ');
    limpo = limpo.replace(/Desenvolvedorade/gi, 'Desenvolvedora de ');
    limpo = limpo.replace(/Desenvolvedorde/gi, 'Desenvolvedor de ');
    limpo = limpo.replace(/Engenheirode/gi, 'Engenheiro de ');
    limpo = limpo.replace(/Especialistade/gi, 'Especialista de ');
    limpo = limpo.replace(/Infraestruturae /gi, 'Infraestrutura e ');
    limpo = limpo.replace(/Infraestruturae/gi, 'Infraestrutura e ');
    limpo = limpo.replace(/Supervisorde/gi, 'Supervisor de ');
    limpo = limpo.replace(/Assistentede/gi, 'Assistente de ');
    limpo = limpo.replace(/Coordenadorde/gi, 'Coordenador de ');
    limpo = limpo.replace(/Gerentede/gi, 'Gerente de ');
    limpo = limpo.replace(/Auxiliarde/gi, 'Auxiliar de ');
    limpo = limpo.replace(/Diretorde/gi, 'Diretor de ');
    limpo = limpo.replace(/Técnicode|Tecnicode/gi, 'Técnico de ');
    limpo = limpo.replace(/Estagiáriode|Estagiariode/gi, 'Estagiário de ');
    limpo = limpo.replace(/TISr/gi, 'TI Sr');
    limpo = limpo.replace(/TIJr/gi, 'TI Jr');
    limpo = limpo.replace(/T\.i/gi, 'TI');
    limpo = limpo.replace(/\s*-\s*/g, ' - '); 
    limpo = limpo.replace(/\s*\(/g, ' ('); 
    return limpo.replace(/\s+/g, ' ').trim();
  };

  const carregarVagas = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:8000/vagas/')
      const vagasMaisNovas = response.data.sort((a, b) => b.id - a.id)
      setVagas(vagasMaisNovas)
    } catch (error) {
      console.error("Erro ao buscar vagas:", error)
    } finally {
      setLoading(false)
    }
  }

  const cadastrarEBuscar = async (e) => {
    e.preventDefault()
    if (!novoTermo) return
    setProcessando(true)
    try {
      await axios.post(`http://127.0.0.1:8000/usuarios/1/termos/`, { palavra_chave: novoTermo })
      const termoSalvo = novoTermo
      setNovoTermo('') 
      await axios.post('http://127.0.0.1:8000/admin/varredura/')
      alert(`Termo '${termoSalvo}' adicionado! A varredura começou. Aguarde...`)
      setTimeout(() => {
        carregarVagas()
        setProcessando(false) 
      }, 8000)
    } catch (error) {
      alert("Erro ao cadastrar ou buscar.");
      setProcessando(false)
    }
  }

  useEffect(() => { carregarVagas() }, [])

  return (
    <div className="min-h-screen bg-[#0b0f1a] text-slate-100 p-6 md:p-12 font-sans">
      <div className="max-w-6xl mx-auto">
        
        <header className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8 mb-12 border-b border-slate-800 pb-10">
          <div className="flex items-center gap-5">
            <div>
              <h1 className="text-3xl font-extrabold tracking-tight italic">Radar de Vagas</h1>
              
              {/* ASSINATURA E LINKS DA EMILLY */}
              <div className="flex flex-col mt-1">
                <p className="text-[10px] font-mono text-blue-400 uppercase tracking-[0.2em] font-bold">
                  Developed by Emilly Yorke
                </p>
                <div className="flex gap-4 mt-2">
                  <a href="https://www.linkedin.com/in/emilly-yorke" target="_blank" rel="noreferrer" className="text-xs text-slate-400 hover:text-white transition-colors flex items-center gap-1">
                    <span>🔗</span> LinkedIn
                  </a>
                  <a href="https://github.com/emillyyorke" target="_blank" rel="noreferrer" className="text-xs text-slate-400 hover:text-white transition-colors flex items-center gap-1">
                    <span>📁</span> GitHub
                  </a>
                </div>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap gap-4 w-full lg:w-auto">
            <form onSubmit={cadastrarEBuscar} className="flex gap-2 flex-grow lg:flex-grow-0">
              <input 
                className="bg-slate-900 border border-slate-700 px-4 py-3 rounded-xl outline-none focus:ring-2 focus:ring-blue-500 transition-all w-full md:w-64"
                value={novoTermo} 
                onChange={(e) => setNovoTermo(e.target.value)}
                placeholder="Ex: Infraestrutura" 
                disabled={processando}
              />
              <button disabled={processando} className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-xl transition-all disabled:opacity-50 text-white font-bold whitespace-nowrap shadow-lg shadow-blue-500/20">
                {processando ? "⏳ Processando..." : "Buscar"}
              </button>
            </form>
          </div>
        </header>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 opacity-50">
            <p className="text-slate-400 text-lg font-medium animate-pulse">⏳ Conectando ao banco de dados...</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {vagas.map(vaga => (
              <div key={vaga.id} className="bg-slate-900/50 border border-slate-800 p-6 rounded-3xl hover:border-blue-500/40 transition-all group hover:bg-slate-900 flex flex-col">
                <div className="bg-blue-500/10 w-10 h-10 rounded-lg flex items-center justify-center mb-4 text-xl">
                  💼
                </div>
                <h3 className="font-bold text-lg mb-6 leading-tight text-slate-100 group-hover:text-blue-400 transition-colors flex-grow">
                  {formatarTitulo(vaga.titulo)}
                </h3>
                <div className="flex items-center justify-between mt-auto">
                  <a href={vaga.link} target="_blank" rel="noreferrer" className="bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 transition-all">
                    Ver detalhes 🔗
                  </a>
                  <span className="text-xs text-slate-600 font-mono">#ID-{vaga.id}</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {vagas.length === 0 && !loading && (
          <div className="text-center py-24 bg-slate-900/30 rounded-3xl border-2 border-dashed border-slate-800">
            <p className="text-slate-500 text-lg">Nenhuma vaga encontrada. Cadastre um termo acima!</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
