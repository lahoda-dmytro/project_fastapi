import React, {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";

const EditPost = () => {
    const {postId} = useParams();
    const navigate = useNavigate();
    const [title, setTitle] = useState("");
    const [body, setBody] = useState("");
    const [authorId, setAuthorId] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/posts/${postId}`)
            .then((res) => {
                if (!res.ok) throw new Error("failed to get post");
                return res.json();
            })
            .then((data) => {
                setTitle(data.title);
                setBody(data.body);
                setAuthorId(data.author_id);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [postId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        try {
            const response = await fetch(`http://127.0.0.1:8000/posts/${postId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, body, author_id: Number(authorId)})
            });
            if (!response.ok) throw new Error("failed to update post");
            setSuccess(true);
            setTimeout(() => navigate("/posts"), 1000);
        } catch (err) {
            setError(err.message);
        }
    };

    if (loading) return <div className="container">loading...</div>;
    if (error) return <div className="container">error: {error}</div>;

    return (
        <div className="container">
            <h2>edit post</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>title: </label>
                    <input value={title} onChange={e => setTitle(e.target.value)} required/>
                </div>
                <div>
                    <label>body: </label>
                    <textarea value={body} onChange={e => setBody(e.target.value)} required/>
                </div>
                <div>
                    <label>author id: </label>
                    <input type="number" value={authorId} onChange={e => setAuthorId(e.target.value)} required/>
                </div>
                <button type="submit">save</button>
            </form>
            {success && <div style={{color: 'green'}}>post updated!</div>}
            {error && <div style={{color: 'red'}}>error: {error}</div>}
        </div>
    );
};

export default EditPost; 