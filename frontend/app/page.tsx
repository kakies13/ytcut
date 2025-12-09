'use client';

import { useState } from 'react';
import axios from 'axios';
import { Scissors, FileVideo, Download, Loader2, Sparkles, Play } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function Home() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(''); // 'downloading', 'transcribing', 'analyzing', 'processing'
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState('');

  const processVideo = async () => {
    if (!url) return;
    setLoading(true);
    setResult(null);
    setError('');
    setStatus('Yapay Zeka Videoyu İnceliyor...');

    try {
      // In a real app, we'd use WebSocket or SSE for real-time status updates
      // Here we just wait for the long request
      const response = await axios.post('http://127.0.0.1:8000/api/process', { url });

      if (response.data.status === 'error') {
        setError(response.data.message || 'Bir hata oluştu.');
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError('Sunucu ile bağlantı kurulamadı.');
      console.error(err);
    } finally {
      setLoading(false);
      setStatus('');
    }
  };

  return (
    <main className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-4 selection:bg-red-500 selection:text-white">
      <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>

      <div className="z-10 w-full max-w-4xl space-y-12">
        {/* Header */}
        <div className="text-center space-y-4">
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="inline-flex items-center justify-center p-3 bg-red-600 rounded-2xl shadow-2xl shadow-red-900/50 mb-4"
          >
            <Scissors className="w-8 h-8 text-white" />
          </motion.div>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter bg-gradient-to-b from-white to-neutral-500 bg-clip-text text-transparent">
            YTcut
          </h1>
          <p className="text-neutral-400 text-lg md:text-xl max-w-2xl mx-auto">
            YouTube videolarını yapay zeka ile saniyeler içinde <span className="text-red-500 font-semibold">Shorts</span> ve <span className="text-pink-500 font-semibold">TikTok</span> kliplerine dönüştürün.
          </p>
        </div>

        {/* Input Area */}
        <motion.div
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="relative max-w-2xl mx-auto"
        >
          <div className="absolute -inset-1 bg-gradient-to-r from-red-600 to-pink-600 rounded-2xl blur opacity-30 animate-pulse"></div>
          <div className="relative flex items-center bg-neutral-900 border border-neutral-800 rounded-xl p-2 shadow-2xl">
            <div className="pl-4 text-neutral-500">
              <FileVideo className="w-6 h-6" />
            </div>
            <input
              type="text"
              placeholder="YouTube videosunun linkini buraya yapıştır..."
              className="flex-1 bg-transparent border-none outline-none text-white px-4 py-4 text-lg placeholder:text-neutral-600"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              disabled={loading}
            />
            <button
              onClick={processVideo}
              disabled={loading || !url}
              className="bg-white text-black hover:bg-neutral-200 disabled:opacity-50 disabled:cursor-not-allowed px-6 py-3 rounded-lg font-semibold transition-all flex items-center gap-2"
            >
              {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Sparkles className="w-5 h-5" />}
              {loading ? 'İşleniyor' : 'Dönüştür'}
            </button>
          </div>
          {status && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center text-neutral-500 mt-4 text-sm font-mono animate-pulse"
            >
              🚀 {status}
            </motion.p>
          )}
          {error && (
            <p className="text-center text-red-500 mt-4 font-medium bg-red-500/10 py-2 rounded-lg border border-red-500/20">{error}</p>
          )}
        </motion.div>

        {/* Results */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={{ opacity: 1, y: 0 }}
              className="space-y-8"
            >
              <div className="flex items-center justify-between text-neutral-400 border-b border-neutral-800 pb-4">
                <h3 className="text-2xl font-semibold text-white">Oluşturulan Klipler (AI)</h3>
                <span className="bg-neutral-800 px-3 py-1 rounded-full text-sm">{result.clips.length} Klip Bulundu</span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {result.clips.map((clip: any, idx: number) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: idx * 0.1 }}
                    className="group relative bg-neutral-900 border border-neutral-800 rounded-2xl overflow-hidden hover:border-neutral-600 transition-all hover:shadow-2xl hover:shadow-red-900/20 cursor-pointer"
                  >
                    {/* Real Video Preview */}
                    <div className="aspect-[9/16] bg-black flex items-center justify-center relative overflow-hidden group-hover:scale-105 transition-transform duration-500">
                      <video
                        src={`http://127.0.0.1:8000/downloads/${clip.file_path}`}
                        className="w-full h-full object-cover"
                        controls
                        preload="metadata"
                      />
                    </div>

                    <div className="absolute inset-x-0 bottom-0 p-4 space-y-2 bg-gradient-to-t from-black/80 to-transparent">
                      <div className="flex items-start justify-between gap-2">
                        <h4 className="font-semibold text-white line-clamp-2 leading-tight">{clip.title}</h4>
                        <span className="text-xs font-mono bg-neutral-800 text-neutral-300 px-2 py-1 rounded">{clip.duration}s</span>
                      </div>
                      <p className="text-xs text-neutral-400 line-clamp-2">{clip.reason}</p>

                      <a
                        href={`http://127.0.0.1:8000/downloads/${clip.file_path}`}
                        download
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center justify-center gap-2 w-full bg-white/10 hover:bg-white text-white hover:text-black mt-2 py-2 rounded-lg font-medium text-sm transition-colors backdrop-blur-sm"
                      >
                        <Download className="w-4 h-4" /> İndir
                      </a>
                    </div>
                  </motion.div>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
