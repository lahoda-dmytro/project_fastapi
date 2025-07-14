import React, {useEffect, useState} from "react";
import {useParams, useNavigate} from "react-router-dom";

const EditUser = () => {
    const {userId} = useParams();
    const navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [age, setAge] = useState("");
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/users/${userId}`)
            .then((res) => {
                if (!res.ok) throw new Error("failed to get user");
                return res.json();
            })
            .then((data) => {
                setUsername(data.username);
                setAge(data.age);
                setLoading(false);
            })
            .catch((err) => {
                setError(err.message);
                setLoading(false);
            });
    }, [userId]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSuccess(false);
        try {
            const response = await fetch(`http://127.0.0.1:8000/users/${userId}`, {
                method: "PUT",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username, age: Number(age)})
            });
            if (!response.ok) throw new Error("failed to update user");
            setSuccess(true);
            setTimeout(() => navigate("/users"), 1000);
        } catch (err) {
            setError(err.message);
        }
    };

    if (loading) return <div className="container">loading...</div>;
    if (error) return <div className="container">error: {error}</div>;

    return (
        <div className="container">
            <h2>edit user</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>user name: </label>
                    <input value={username} onChange={e => setUsername(e.target.value)} required/>
                </div>
                <div>
                    <label>age: </label>
                    <input type="number" value={age} onChange={e => setAge(e.target.value)} required/>
                </div>
                <button type="submit">save</button>
            </form>
            {success && <div style={{color: 'green'}}>user updated!</div>}
            {error && <div style={{color: 'red'}}>error: {error}</div>}
        </div>
    );
};

export default EditUser; 