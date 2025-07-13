import React, {useState} from "react";

const AddUser = () => {
    const [username, setUsername] = useState("");
    const [age, setAge] = useState("");
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setResult(null);
        try {
            const response = await fetch("http://127.0.0.1:8000/users/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({username, age: Number(age)})
            });
            if (!response.ok)
                throw new Error("failed to create user");
            const data = await response.json();
            setResult(data);
            setUsername("");
            setAge("");
        } catch (err) {
            setError(err.message);
        }
    };

    return (
        <div className="container">
            <h2>create author</h2>
            <form onSubmit={handleSubmit}>
                <div>
                    <label>user name: </label>
                    <input value={username} onChange={e => setUsername(e.target.value)} required/>
                </div>
                <div>
                    <label>age: </label>
                    <input type="number" value={age} onChange={e => setAge(e.target.value)} required/>
                </div>
                <button type="submit">create author</button>
            </form>
            {result && <div>author created: {result.username} (ID: {result.id})</div>}
            {error && <div style={{color: 'red'}}>error: {error}</div>}
        </div>
    );
};

export default AddUser;
