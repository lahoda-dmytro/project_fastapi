import React from "react";
import {useParams, Link} from "react-router-dom";
import {useFetch} from "./useFetch";

const PostDetail = () => {
    const {postId} = useParams();
    const {data: post, loading, error} = useFetch(`http://127.0.0.1:8000/posts/${postId}`);

    if (loading) return <div className="container">loading...</div>;
    if (error) return <div className="container">error: {error}</div>;
    if (!post) return <div className="container">post not found</div>;

    return (
        <div className="container">
            <h2>post detail</h2>
            <p><strong>title:</strong> {post.title}</p>
            <p><strong>body:</strong> {post.body}</p>
            <p><strong>author id:</strong> {post.author_id}</p>
            <Link to="/posts">back to posts</Link>
        </div>
    );
};

export default PostDetail; 