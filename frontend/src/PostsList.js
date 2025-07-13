import React, {useEffect, useState} from "react";

const PostsList = () => {
    const [posts, setPosts] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
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
    }, []);

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
                        <li key={post.id}>
                            <strong>{post.title}</strong> — {post.body} (author id: {post.author_id})
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default PostsList;
