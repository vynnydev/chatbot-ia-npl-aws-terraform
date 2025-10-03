import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'El Sabor - Chatbot',
  description: 'Chatbot para Restaurante Mexicano',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  );
}