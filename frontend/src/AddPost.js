import React from "react";
import {useForm} from "react-hook-form";

function AddPost() {
    const {register, handleSubmit, reset, formState: {errors, isSubmitSuccessful}} = useForm();

    const onSubmit = async (data) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/posts/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    title: data.title,
                    body: data.body,
                    author_id: Number(data.author_id)
                })
            });
            if (response.ok) reset();
        } catch (err) {
        }
    };

    return (
        <div className="container">
            <h2>create new post</h2>
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
                <button type="submit">create post</button>
                {isSubmitSuccessful && <div style={{color: 'green'}}>post created!</div>}
            </form>
        </div>
    );
}

export default AddPost;