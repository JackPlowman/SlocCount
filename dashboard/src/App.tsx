function App() {
  return (
    <div className="min-h-screen w-full relative bg-white">
      {/* Orange Soft Glow - Inverted Circle */}
      <div
        className="absolute inset-0 z-0"
        style={{
          backgroundImage: `
          radial-gradient(circle at center, transparent 0%, #FF7112 100%)
        `,
          opacity: 0.3,
          mixBlendMode: "multiply",
        }}
      />
    </div>
  );
}

export default App;
