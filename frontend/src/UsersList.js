import React from "react";
import {Link} from "react-router-dom";
import {useFetch} from "./useFetch";

const UsersList = () => {
    const {data: users, loading, error} = useFetch("http://127.0.0.1:8000/users/");
    const [deleting, setDeleting] = React.useState(null);
    const [localError, setLocalError] = React.useState(null);

    const fetchUsers = () => {
        window.location.reload();
    };

    const handleDelete = async (id) => {
        setDeleting(id);
        try {
            const res = await fetch(`http://127.0.0.1:8000/users/${id}`, {
                method: "DELETE"
            });
            if (!res.ok) throw new Error("failed to delete user");
            fetchUsers();
        } catch (err) {
            setLocalError(err.message);
        } finally {
            setDeleting(null);
        }
    };

    if (loading) return <div className="container">loading...</div>;
    if (error || localError) return <div className="container">error: {error || localError}</div>;

    return (
        <div className="container">
            <h2>list of users</h2>
            {(!users || users.length === 0) ? (
                <p>haven't users yet</p>
            ) : (
                <ul>
                    {users.map((user) => (
                        <li key={user.id}
                            style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                            <span>{user.username} (age: {user.age}, id: {user.id})</span>
                            <div className="list-btn-group">
                                <Link to={`/users/${user.id}/edit`}>
                                    <button type="button" className="list-btn">edit</button>
                                </Link>
                                <button onClick={() => handleDelete(user.id)} disabled={deleting === user.id}
                                        className="list-btn">
                                    {deleting === user.id ? 'deleting...' : 'delete'}
                                </button>
                            </div>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default UsersList; 