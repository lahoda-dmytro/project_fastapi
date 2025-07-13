import React, {useState} from "react";

const AddPost = () => {
    const [title, setTitle] = useState("");
    const [body, setBody] = useState("");
    const [authorId, setAuthorId] = useState("");
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setResult(null);
        try {
            const response = await fetch("http://127.0.0.1:8000/posts/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({title, body, author_id: Number(authorId)})
            });
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail);
            }
            const data = await response.json();
            setResult(data);
            setTitle("");
            setBody("");
            setAuthorId("");
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div>
            <h2>create new post</h2>
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
                <button type="submit">create post</button>
            </form>
            {result && <div>post created: {result.title} (ID: {result.id})</div>}
            {error && <div style={{color: 'red'}}>error: {error}</div>}
        </div>
    );
};

export default AddPost;
