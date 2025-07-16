import React from "react";
import {useForm} from "react-hook-form";

function AddUser() {
    const {register, handleSubmit, reset, formState: {errors, isSubmitSuccessful}, setError} = useForm();

    const onSubmit = async (data) => {
        try {
            const response = await fetch("http://127.0.0.1:8000/users/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                const errorData = await response.json();
                let msg = "";
                if (Array.isArray(errorData.detail)) {
                    msg = errorData.detail.map(e => e.msg).join("; ");
                } else {
                    msg = errorData.detail || "creating user error";
                }
                setError("age", {type: "manual", message: msg});
                return;
            }
            reset();
        } catch (err) {
            setError("age", {type: "manual", message: err.message});
        }
    };

    return (
        <div className="container">
            <h2>create new user</h2>
            <form onSubmit={handleSubmit(onSubmit)}>
                <div>
                    <label>user name: </label>
                    <input {...register("username", {required: "input username"})} />
                    {errors.username && <span style={{color: "red"}}>{errors.username.message}</span>}
                </div>
                <div>
                    <label>age: </label>
                    <input type="number" {...register("age", {required: "input age"})} />
                    {errors.age && <span style={{color: "red"}}>{errors.age.message}</span>}
                </div>
                <button type="submit">create user</button>
                {isSubmitSuccessful && <div style={{color: 'green'}}>user created!</div>}
            </form>
        </div>
    );
}

export default AddUser;