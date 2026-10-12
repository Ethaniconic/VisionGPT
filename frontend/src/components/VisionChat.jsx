import React, { useState } from 'react'
import { askQuestion } from '../services/api';

const VisionChat = ({selectedFile}) => {
    const [file, setFile] = useState(null);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const handleAsk = async (e) => {
        e.preventDefault();
        if (!selectedFile || !question.trim()){
            setError("Please select an image first and enter a question.");
            return;
        }

        setLoading(true);
        setError("");
        setAnswer("");

        try {
            const data = await askQuestion(selectedFile, question);
            setAnswer(data.answer);
        } catch (error) {
            setError(error.message || "Failed to get an answer");
        } finally {
            setLoading(false);
        }
    }

  return (
        <div style={{ maxWidth: '500px', width: '100%', margin: '0 auto', padding: '20px', border: '1px solid #ccc' }}>
            <h2>Vision GPT Chat</h2>
            <form onSubmit={handleAsk}>
                <div style={{ marginBottom: '10px' }}>
                    <input 
                        type="text" 
                        placeholder="Ask a question about the uploaded image..." 
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        style={{ width: '100%', padding: '8px' }}
                    />
                </div>
                <button type="submit" disabled={loading || !selectedFile}>
                    {loading ? "Thinking..." : "Ask"}
                </button>
            </form>
            {error && <p style={{ color: 'red', marginTop: '10px' }}>{error}</p>}
            {answer && (
                <div style={{ marginTop: '20px', background: '#f4f4f4', padding: '10px' }}>
                    <strong>Answer:</strong>
                    <p>{answer}</p>
                </div>
            )}
        </div>
    );
}

export default VisionChat