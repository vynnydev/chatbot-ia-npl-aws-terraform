import ChatInterface from '../components/ChatInterface';
import Header from '../components/Header';

export default function Home() {
  return (
    <div className="flex flex-col h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <Header />
      <ChatInterface />
    </div>
  );
}