"use client";

import { useEffect, useRef, useState } from "react";
import { toast } from "react-hot-toast";

import { Button } from "@/components/ui/button";

const API_URL = process.env.API_URL || process.env.NEXT_PUBLIC_API_URL;

interface ChatProps {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any;
}

interface ChatHistoryMessage {
  role: string;
  content: string;
}

const Chat = ({ data }: ChatProps) => {
  const [chatHistory, setChatHistory] = useState<ChatHistoryMessage[]>([]);
  const [chatInput, setChatInput] = useState("");
  const [loading, setLoading] = useState(false);
  const _cancel = useRef<boolean>(false);
  const _windowScroll = useRef<number>(0);

  useEffect(() => {
    const handleScroll = () => {
      _windowScroll.current = window.scrollY;
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleSendMessage = async () => {
    setLoading(true);

    if (chatInput.trim() === "") {
      toast.error("Please enter a message");
      setLoading(false);
      return;
    }

    setChatInput("");
    setChatHistory((prev: ChatHistoryMessage[]) => [
      ...prev, 
      { role: 'user', content: chatInput },
      { role: 'assistant', content: '' }
    ]);

    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: {
        'Accept': 'text/event-stream'
      },
      body: JSON.stringify({
        history: [
          ...chatHistory,
          { role: 'user', content: chatInput }
        ],
        message: chatInput
      })
    });

    const reader = response.body?.getReader();
    if (!reader) {
      setLoading(false);
      return;
    }

    while (true) {
      const { done, value } = await reader.read();
      if (done || _cancel.current) {
        _cancel.current = false;
        console.log('Done');
        break;
      }
      
      // Convert the chunk to text and append to message
      const chunk = new TextDecoder().decode(value);
      setChatHistory((prev: ChatHistoryMessage[]) => {
        const lastMessage = prev[prev.length - 1];
        const newMessage = (lastMessage?.content || "") + chunk;
        return [...prev.slice(0, -1), { ...lastMessage, content: newMessage }];
      });

      setTimeout(() => {
        if (_windowScroll.current === window.scrollY) {
          window.scrollTo(0, document.body.scrollHeight);
        }
      }, 0);
    }

    setLoading(false);
  };

  return (
    <div className="max-w-[800px] mx-auto">
      <div className="flex flex-col h-screen p-4">
        <div className="flex-1 space-y-4 pb-4">
          {chatHistory.map((msg, i) => (
            <div key={i} className="flex gap-3 p-4 border rounded-lg">
              <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center text-primary-foreground">
                {msg.role === 'user' ? 'U' : 'A'}
              </div>
              <div className="flex-1">
                <p className="text-sm text-muted-foreground">
                  {msg.role === 'user' ? 'User' : 'Assistant'}
                </p>
                <p className="mt-1">{msg.content}</p>
              </div>
            </div>
          ))}
        </div>

        <div className="border-t py-4 sticky bottom-0 bg-background">
          <form 
            onSubmit={(e) => {
              e.preventDefault();
              handleSendMessage();
            }}
            className="flex gap-2"
          >
            <input
              type="text"
              placeholder="Type your message..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              className="flex-1 p-2 border rounded-md"
            />
            <div className="flex gap-2">
              <Button type="submit" disabled={loading}>
                {loading ? 'Sending...' : 'Send'}
              </Button>
              {loading && (
                <Button 
                  type="button" 
                  variant="outline"
                  onClick={() => {
                    _cancel.current = true;
                  }}
                >
                  Cancel
                </Button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}


export default Chat;
