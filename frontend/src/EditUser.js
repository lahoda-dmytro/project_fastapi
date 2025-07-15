import React, {useEffect} from "react";
import {useForm} from "react-hook-form";
import {useParams, useNavigate} from "react-router-dom";

const EditUser = () => {
    const {userId} = useParams();
    const navigate = useNavigate();
    const {register, handleSubmit, reset, setError, formState: {errors, isSubmitSuccessful, isSubmitting}} = useForm();

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/users/${userId}`)
            .then((res) => {
                if (!res.ok) throw new Error("failed to get user");
                return res.json();
            })
            .then((data) => {
                reset({username: data.username, age: data.age});
            })
            .catch((err) => {
                setError("root", {type: "manual", message: err.message});
            });
    }, [userId, reset, setError]);

    const onSubmit = async (data) => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });
            if (!response.ok) throw new Error("failed to update user");
            setTimeout(() => navigate("/users"), 1000);
        } catch (err) {
            setError("root", {type: "manual", message: err.message});
        }
    };

    return (
        <div className="container">
            <h2>edit user</h2>
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
                <button type="submit" disabled={isSubmitting}>save</button>
                {isSubmitSuccessful && <div style={{color: 'green'}}>user updated!</div>}
                {errors.root && <div style={{color: 'red'}}>{errors.root.message}</div>}
            </form>
        </div>
    );
};

export default EditUser; 