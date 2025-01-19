import { useState, useEffect } from "react";
import api from "../api"; // Make sure your api instance is set up
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Notes from "../components/Notes";
import "../styles/Home.css";

export default function Home() {
  const [notes, setNotes] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");

  const getNotes = async () => {
    try {
      const response = await api.get("/api/notes/");
      setNotes(response.data); // Set fetched notes to state
      console.log(response.data);
    } catch (err) {
      alert(err);
    }
  };

  // Fetch notes on component mount

  useEffect(() => {
    getNotes(); // Call the async fetch function
  }, []); // Empty dependency array means this effect runs only once on mount

  const deleteNote = async (id) => {
    try {
      const response = await api.delete(`/api/notes/delete/${id}/`);
      if (response.status === 204) {
        toast.success("Note deleted!");
      } else {
        toast.error("Failed to delete note.");
      }
      getNotes();
    } catch (error) {
      alert(err);
    }
  };

  const createNote = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/api/notes/", { content, title });
      if (response.status === 201) {
        toast.success("Note created!");
      } else {
        toast.error("Failed to create note.");
      }
      getNotes();
    } catch (err) {
      alert(err);
    }
  };

  return (
    <div>
      <ToastContainer />
      <div>
        <h2>Notes</h2>
        {notes.map((note) => (
          <Notes key={note.id} note={note} onDelete={deleteNote} />
        ))}
      </div>
      <h2>Create a Note</h2>
      <form onSubmit={createNote}>
        <label htmlFor="title">Title: </label>
        <br />
        <input
          id="title"
          type="text"
          name="title"
          value={title}
          required
          onChange={(e) => setTitle(e.target.value)}
        />
        <label htmlFor="content">Content: </label>
        <br />
        <textarea
          id="content"
          value={content}
          required
          name="content"
          onChange={(e) => setContent(e.target.value)}
        />
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}
