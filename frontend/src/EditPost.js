import React, {useEffect} from "react";
import {useForm} from "react-hook-form";
import {useParams, useNavigate} from "react-router-dom";

const EditPost = () => {
    const {postId} = useParams();
    const navigate = useNavigate();
    const {register, handleSubmit, reset, setError, formState: {errors, isSubmitSuccessful, isSubmitting}} = useForm();

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/posts/${postId}`)
            .then((res) => {
                if (!res.ok) throw new Error("failed to get post");
                return res.json();
            })
            .then((data) => {
                reset({title: data.title, body: data.body, author_id: data.author_id});
            })
            .catch((err) => {
                setError("root", {type: "manual", message: err.message});
            });
    }, [postId, reset, setError]);

    const onSubmit = async (data) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/posts/${postId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    title: data.title,
                    body: data.body,
                    author_id: Number(data.author_id)
                })
            });
            if (!response.ok) throw new Error("failed to update post");
            setTimeout(() => navigate("/posts"), 1000);
        } catch (err) {
            setError("root", {type: "manual", message: err.message});
        }
    };

    return (
        <div className="container">
            <h2>edit post</h2>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <label>title: </label>
                    <input {...register("title", {required: "input title"})} />
                    {errors.title && <span style={{color: "red"}}>{errors.title.message}</span>}
                </div>
                <div>
                    <label>body: </label>
                    <textarea {...register("body", {required: "input text"})} />
                    {errors.body && <span style={{color: "red"}}>{errors.body.message}</span>}
                </div>
                <div>
                    <label>author id: </label>
                    <input type="number" {...register("author_id", {required: "input author id"})} />
                    {errors.author_id && <span style={{color: "red"}}>{errors.author_id.message}</span>}
                </div>
                <button type="submit" disabled={isSubmitting}>save</button>
                {isSubmitSuccessful && <div style={{color: 'green'}}>post updated!</div>}
                {errors.root && <div style={{color: 'red'}}>{errors.root.message}</div>}
            </form>
        </div>
    );
};

export default EditPost; 