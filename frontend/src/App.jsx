import React, { useState, useEffect } from 'react';
import { userService, postService, roleService } from './services/api';
import { Plus, Users, Layout, FileText, Trash2, Github, Star, ChevronDown } from 'lucide-react';
import './App.css';

function App() {
  const [activeTab, setActiveTab] = useState('posts');
  const [posts, setPosts] = useState([]);
  const [users, setUsers] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showUserModal, setShowUserModal] = useState(false);
  const [showPostModal, setShowPostModal] = useState(false);
  const [showRoleModal, setShowRoleModal] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [postsRes, usersRes, rolesRes] = await Promise.all([
        postService.getAll(),
        userService.getAll(),
        roleService.getAll()
      ]);
      setPosts(postsRes.data);
      setUsers(usersRes.data);
      setRoles(rolesRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const getActivity = () => {
    const activity = [];
    posts.forEach(p => {
      const author = users.find(u => u.id === p.author_id);
      activity.push({
        id: `post-${p.id}`,
        user: author ? author.username : `User #${p.author_id}`,
        text: `created a new post: "${p.title}"`,
        date: new Date(p.created_at)
      });
    });
    users.forEach(u => {
      activity.push({
        id: `user-${u.id}`,
        user: u.username,
        text: `joined the project`,
        date: new Date(u.created_at)
      });
    });
    return activity.sort((a, b) => b.date - a.date).slice(0, 8);
  };

  const formatTimeAgo = (date) => {
    const seconds = Math.floor((new Date() - date) / 1000);
    if (seconds < 60) return `${seconds}s ago`;
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60) return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days} days ago`;
  };

  const handleDeletePost = async (id) => {
    if (confirm('Are you sure you want to delete this post?')) {
      await postService.delete(id);
      setPosts(posts.filter(p => p.id !== id));
    }
  };

  const handleDeleteUser = async (id) => {
    if (confirm('Are you sure you want to delete this user?')) {
      await userService.delete(id);
      fetchData();
    }
  };

  return (
    <div className="app-layout">
      {/* Sidebar Left */}
      <aside className="sidebar">
        <div className="sidebar-title">Top repositories</div>
        <nav className="nav-list">
          <button className={`nav-item ${activeTab === 'posts' ? 'active' : ''}`} onClick={() => setActiveTab('posts')}>
            <FileText size={16} className="nav-icon" /> lahoda-dmytro/posts
          </button>
          <button className={`nav-item ${activeTab === 'users' ? 'active' : ''}`} onClick={() => setActiveTab('users')}>
            <Users size={16} className="nav-icon" /> lahoda-dmytro/users
          </button>
          <button className={`nav-item ${activeTab === 'roles' ? 'active' : ''}`} onClick={() => setActiveTab('roles')}>
            <Layout size={16} className="nav-icon" /> lahoda-dmytro/roles
          </button>
        </nav>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="content-header">
          <h1>{activeTab === 'posts' ? 'Feed' : activeTab.charAt(0).toUpperCase() + activeTab.slice(1)}</h1>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button className="primary" onClick={() => {
              if (activeTab === 'posts') setShowPostModal(true);
              else if (activeTab === 'users') setShowUserModal(true);
              else setShowRoleModal(true);
            }}>
              <Plus size={16} /> New {activeTab.slice(0, -1)}
            </button>
          </div>
        </header>

        {loading ? (
          <div style={{ color: 'var(--color-fg-muted)' }}>Loading activity...</div>
        ) : (
          <div className="feed">
            {activeTab === 'posts' && posts.map(post => {
              const colors = ['#f1e05a', '#563d7c', '#e34c26', '#3572A5'];
              const color = colors[post.id % colors.length];
              return (
                <div key={post.id} className="card">
                  <div className="card-header">
                    <div className="card-title">lahoda-dmytro/{post.title.toLowerCase().replace(/\s+/g, '_')}</div>
                    <div style={{ display: 'flex', gap: '4px' }}>
                      <button className="star-btn"><Star size={14} /> Star <ChevronDown size={14} /></button>
                      <button onClick={() => handleDeletePost(post.id)} className="delete-btn-minimal"><Trash2 size={14} /></button>
                    </div>
                  </div>
                  <div className="card-body">{post.body}</div>
                  <div className="card-footer">
                    <span className="lang-dot" style={{ backgroundColor: color }}></span>
                    <span>Author: {users.find(u => u.id === post.author_id)?.username || `user_${post.author_id}`}</span>
                    <span>•</span>
                    <span>{formatTimeAgo(new Date(post.created_at))}</span>
                  </div>
                </div>
              );
            })}

            {activeTab === 'users' && users.map(user => (
              <div key={user.id} className="card">
                <div className="card-header">
                  <div className="card-title">{user.username}</div>
                  <button onClick={() => handleDeleteUser(user.id)} className="delete-btn-minimal"><Trash2 size={14} /></button>
                </div>
                <div className="card-body">Member of this space since {new Date(user.created_at).toLocaleDateString()}.</div>
                <div className="card-footer">
                  <div style={{ display: 'flex', gap: '6px' }}>
                    {user.roles.map(role => (
                      <span key={role.id} style={{ border: '1px solid var(--color-border-default)', padding: '0 10px', borderRadius: '12px', fontSize: '12px' }}>{role.name}</span>
                    ))}
                  </div>
                  <span>•</span>
                  <span>Age: {user.age}</span>
                </div>
              </div>
            ))}

            {activeTab === 'roles' && roles.map(role => (
              <div key={role.id} className="card">
                <div className="card-header">
                  <div className="card-title">{role.name}</div>
                </div>
                <div className="card-body">Permission group with ID: {role.id}</div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Activity Sidebar Right */}
      <aside className="activity-sidebar">
        <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '16px' }}>Latest from our changelog</div>
        <div className="timeline">
          {getActivity().map(item => (
            <div key={item.id} className="timeline-item">
              <div className="timeline-dot"></div>
              <div className="timeline-date">{formatTimeAgo(item.date)}</div>
              <div className="timeline-text">
                <strong>{item.user}</strong> {item.text}
              </div>
            </div>
          ))}
          {getActivity().length === 0 && <div className="timeline-text" style={{ color: 'var(--color-fg-muted)' }}>No recent activity found.</div>}
        </div>
      </aside>

      {/* Modals */}
      {showPostModal && <PostModal onClose={() => setShowPostModal(false)} onSuccess={fetchData} users={users} />}
      {showUserModal && <UserModal onClose={() => setShowUserModal(false)} onSuccess={fetchData} roles={roles} />}
      {showRoleModal && <RoleModal onClose={() => setShowRoleModal(false)} onSuccess={fetchData} />}
    </div>
  );
}

// Reuse Modals from previous version but update styles slightly to match
function PostModal({ onClose, onSuccess, users }) {
  const [formData, setFormData] = useState({ title: '', body: '', author_id: users[0]?.id || '' });
  const handleSubmit = async (e) => {
    e.preventDefault();
    await postService.create(formData);
    onSuccess();
    onClose();
  };
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Create new post</div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Title</label>
            <input value={formData.title} onChange={e => setFormData({ ...formData, title: e.target.value })} required style={{ width: '100%' }} />
          </div>
          <div className="form-group">
            <label className="form-label">Body</label>
            <textarea value={formData.body} onChange={e => setFormData({ ...formData, body: e.target.value })} required rows={4} style={{ width: '100%' }} />
          </div>
          <div className="form-group">
            <label className="form-label">Author</label>
            <select value={formData.author_id} onChange={e => setFormData({ ...formData, author_id: parseInt(e.target.value) })} required style={{ width: '100%' }}>
              {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
            </select>
          </div>
          <div className="modal-footer">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" className="primary">Create post</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function UserModal({ onClose, onSuccess, roles }) {
  const [formData, setFormData] = useState({ username: '', age: '', password: '', roles: [] });
  const handleSubmit = async (e) => {
    e.preventDefault();
    await userService.create({ ...formData, age: parseInt(formData.age), roles: formData.roles.map(Number) });
    onSuccess();
    onClose();
  };
  const toggleRole = (id) => {
    setFormData(prev => ({
      ...prev,
      roles: prev.roles.includes(id) ? prev.roles.filter(r => r !== id) : [...prev.roles, id]
    }));
  };
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Create new user</div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Username</label>
            <input value={formData.username} onChange={e => setFormData({ ...formData, username: e.target.value })} required style={{ width: '100%' }} />
          </div>
          <div className="form-group">
            <label className="form-label">Age</label>
            <input type="number" value={formData.age} onChange={e => setFormData({ ...formData, age: e.target.value })} required style={{ width: '100%' }} />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input type="password" value={formData.password} onChange={e => setFormData({ ...formData, password: e.target.value })} required style={{ width: '100%' }} />
          </div>
          <div className="form-group">
            <label className="form-label">Roles</label>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
              {roles.map(role => (
                <button
                  key={role.id}
                  type="button"
                  className={formData.roles.includes(role.id) ? 'active' : ''}
                  style={{ border: '1px solid var(--color-border-default)', padding: '2px 8px', borderRadius: '12px', fontSize: '12px', background: formData.roles.includes(role.id) ? '#161b22' : 'none' }}
                  onClick={() => toggleRole(role.id)}
                >
                  {role.name}
                </button>
              ))}
            </div>
          </div>
          <div className="modal-footer">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" className="primary">Create user</button>
          </div>
        </form>
      </div>
    </div>
  );
}

function RoleModal({ onClose, onSuccess }) {
  const [name, setName] = useState('');
  const handleSubmit = async (e) => {
    e.preventDefault();
    await roleService.create({ name });
    onSuccess();
    onClose();
  };
  return (
    <div className="modal-overlay">
      <div className="modal">
        <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>Create new role</div>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Role name</label>
            <input value={name} onChange={e => setName(e.target.value)} required style={{ width: '100%' }} />
          </div>
          <div className="modal-footer">
            <button type="button" onClick={onClose}>Cancel</button>
            <button type="submit" className="primary">Create role</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
