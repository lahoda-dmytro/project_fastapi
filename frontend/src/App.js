import {BrowserRouter as Router, Routes, Route, Link} from "react-router-dom";
import './App.css';
import MainPage from "./MainPage";
import PostsList from "./PostsList";
import AddPost from "./AddPost";
import AddUser from "./AddUser";

function App() {
    return (
        <Router>
            <nav>
                <Link to="/">main</Link> | <Link to="/posts">posts</Link> | <Link to="/add-post">add post</Link> | <Link
                to="/add-user">add author</Link>
            </nav>
            <Routes>
                <Route path="/" element={<MainPage/>}/>
                <Route path="/posts" element={<PostsList/>}/>
                <Route path="/add-post" element={<AddPost/>}/>
                <Route path="/add-user" element={<AddUser/>}/>
            </Routes>
        </Router>
    );
}


export default App;
