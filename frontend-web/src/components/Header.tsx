interface HeaderProps {
    title?: string;
    subtitle?: string;
  }
  
  export default function Header({ 
    title = "El Sabor", 
    subtitle = "Restaurante Mexicano" 
  }: HeaderProps) {
    return (
      <header className="bg-gradient-to-r from-primary to-accent text-white p-4 shadow-lg">
        <div className="max-w-4xl mx-auto flex items-center gap-3">
          <div className="text-4xl animate-bounce">🌮</div>
          <div>
            <h1 className="text-2xl font-bold">{title}</h1>
            <p className="text-sm opacity-90">{subtitle}</p>
          </div>
        </div>
      </header>
    );
}