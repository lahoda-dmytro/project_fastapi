import React, {useEffect, useState} from "react";
import {useParams, Link} from "react-router-dom";

const PostDetail = () => {
    const {postId} = useParams();
    const [post, setPost] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/posts/${postId}`)
            .then((res) => {
                if (!res.ok) throw new Error("failed to get post");
                return res.json();
            })
            .then((data) => {
                setPost(data);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [postId]);

    if (loading) return <div className="container">loading...</div>;
    if (error) return <div className="container">error: {error}</div>;
    if (!post) return <div className="container">post not found</div>;

    return (
        <div className="container">
            <h2>Post detail</h2>
            <p><strong>Title:</strong> {post.title}</p>
            <p><strong>Body:</strong> {post.body}</p>
            <p><strong>Author id:</strong> {post.author_id}</p>
            <Link to="/posts">Back to posts</Link>
        </div>
    );
};

export default PostDetail; 