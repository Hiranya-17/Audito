import sampleAlbum from './assets/albumCoverPH.svg'
import logo from './assets/auditoMain.svg'
import { useEffect, useState } from 'react'

function MenuBar() {
    return(
        <header className="site-header">
            <nav className="navbar" aria-label="Main Navigation">
                <a className="logo-link" href="/">
                    <img className="site-logo" src={logo} alt="Audito Home" />
                </a>
                <a className="nav-link" href="/">HOME</a>
                <a className="nav-link account-link" href="/signin"> SIGN IN </a>
            </nav>
        </header>
    )
}

function SongCard({ song }) {
    return (
        <article className="song-card">
            <img
                className="album-image"
                src={song.albumImage || sampleAlbum}
                alt={`${song.title} album cover`}
            />

            <div className="song-info">
                <h2>
                    <a className="song-title-link" href={'/songs/${endureURIComponent(song.id)}'}>
                        {song.title}
                    </a>
                </h2>
                <p className="song-artist">
                    <a className="song-artist-link" href={'/artists/${endureURIComponent(song.artist)}'}>
                        {song.artist}
                    </a>
                    {song.genre && (
                        <a className="song-genre" href={`/genres/${encodeURIComponent(song.genre)}`}>
                            {song.genre}
                        </a>
                    )}
                </p>
                <p className="song-rating">Rating: {song.rating ?? "-"}</p>
            </div>
        </article>
    )
}

function Recommendations() {
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
        <main className="home">
            <h1>RECOMMENDATION</h1>
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
    )
}

function SignIn() {
    return (
        <main className="home">
            <h1>Sign in to Audito</h1>
            <button type="button" disabled>Continue with Google</button>
            <button type="button" disabled>Continue with Apple</button>
        </main>
    )
}

function Profile() {
    return (
        <main className="home">
            <h1>Profile Page</h1>
            <p>Sign in to see your profile.</p>
            <a href="/signin">Sign in</a>
        </main>
    )
}

/*Actual Page Calling*/
export default function App() {
    const path = window.location.pathname
    let page = <Recommendations />

    if (path === '/signin') {
        page = <SignIn />
    } else if (path === '/profile') {
        page = <Profile />
    }

    return (
        <>
            <MenuBar />
            {page}
        </>
    )
}