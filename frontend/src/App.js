import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import './App.css';
import MainPage from "./MainPage";
import PostsList from "./PostsList";
import AddPost from "./AddPost";
import AddUser from "./AddUser";
import UsersList from "./UsersList";
import EditPost from "./EditPost";
import EditUser from "./EditUser";
import PostDetail from "./PostDetail";

function App() {
    return (
        <Router>
            <nav>
                <Link to="/">main</Link> | <Link to="/posts">posts</Link> | <Link to="/add-post">add post</Link> | <Link
                to="/add-user">add user</Link> | <Link to="/users">users</Link>
            </nav>
            <Routes>
                <Route path="/" element={<MainPage/>}/>
                <Route path="/posts" element={<PostsList/>}/>
                <Route path="/add-post" element={<AddPost/>}/>
                <Route path="/add-user" element={<AddUser/>}/>
                <Route path="/users" element={<UsersList/>}/>
                <Route path="/posts/:postId/edit" element={<EditPost/>}/>
                <Route path="/users/:userId/edit" element={<EditUser/>}/>
                <Route path="/posts/:postId" element={<PostDetail/>}/>
            </Routes>
        </Router>
    );
}


export default App;
