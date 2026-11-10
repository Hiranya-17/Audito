import sampleAlbum from './assets/dummyAlbumCover.png'
import logo from './assets/logos/logoWhiteFull.svg'
import { useEffect, useState } from 'react'

function SongCard({ song }) {
    return (
        <article className="song-card">
            <img
                className="album-image"
                src={song.albumImage || sampleAlbum}
                alt={`${song.title} album cover`}
            />

            <div className="song-info">
                <h2>{song.title}</h2>
                <p className="song-artist">{song.artist}</p>
                <p className="song-rating">Rating: {song.rating ?? "-"}</p>
            </div>
        </article>
    )
}

export default function App() {
    const [songs, setSongs] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState('')

    useEffect(() => {
    const controller = new AbortController()

    async function loadSongs() {
        try {
        const response = await fetch('/api/recommendations', {
            signal: controller.signal
        })

        if (!response.ok) {
            throw new Error('Failed to call data.')
        }

        const data = await response.json()
        setSongs(data)
        } catch (err) {
        if (err.name !== 'AbortError') {
            setError('Failed to call data. Please check PY server.')
        }
        } finally {
        if (!controller.signal.aborted) {
            setLoading(false)
        }
        }
    }

    loadSongs()

    return () => controller.abort()
    }, [])
    return (
        <>
            <header className="site-header">
                <nav className="navbar" aria-label="Main Navigation">
                    <a className="logo-link" href="/">
                        <img className="site-logo" src={logo} alt="Audito Home" />
                    </a>
                    <a className="nav-link" href="/">Home</a>
                </nav>
            </header>
            <main className="home">
                <h1>FOR YOU</h1>
                <p>Recommended songs for you.</p>

                {loading && <p>Loading recommendations...</p>}
                {error && <p role="alert">{error}</p>}

                {!loading && !error && songs.length === 0 && (
                <p>No recommendations found.</p>
                )}

                <div className="song-grid">
                {songs.map((song) => (
                    <SongCard key={song.id} song={song} />
                ))}
                </div>
            </main>
        </>
    )
}