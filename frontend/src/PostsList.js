import React, {useEffect, useState} from "react";
import {Link} from "react-router-dom";

const PostsList = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [deleting, setDeleting] = useState(null);

    const fetchPosts = () => {
        setLoading(true);
        fetch("http://127.0.0.1:8000/posts/")
            .then((res) => {
                if (!res.ok) throw new Error("failed to get posts");
                return res.json();
            })
            .then((data) => {
                setPosts(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    };

    useEffect(() => {
        fetchPosts();
    }, []);

    const handleDelete = async (id) => {
        setDeleting(id);
        try {
            const res = await fetch(`http://127.0.0.1:8000/posts/${id}`, {
                method: "DELETE"
            });
            if (!res.ok) throw new Error("failed to delete post");
            fetchPosts();
        } catch (err) {
            setError(err.message);
        } finally {
            setDeleting(null);
        }
    };

    if (loading) return <div className="container">loading...</div>;
    if (error) return <div className="container">error: {error}</div>;

    return (
        <div className="container">
            <h2>list of posts</h2>
            {posts.length === 0 ? (
                <p>haven`t posts yet</p>
            ) : (
                <ul>
                    {posts.map((post) => (
                        <li key={post.id}
                            style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                            <span>
                                <Link to={`/posts/${post.id}`} className="post-link">
                                    <strong>{post.title}</strong>
                                </Link> — {post.body} (author id: {post.author_id})
                            </span>
                            <div className="list-btn-group">
                                <Link to={`/posts/${post.id}/edit`}>
                                    <button type="button" className="list-btn">edit</button>
                                </Link>
                                <button onClick={() => handleDelete(post.id)} disabled={deleting === post.id}
                                        className="list-btn">
                                    {deleting === post.id ? 'deleting...' : 'delete'}
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default PostsList;
