/**
 * Renders a full-screen background with a radial gradient effect.
 *
 * The gradient transitions from transparent at the center to a solid orange (#FF7112) at the edges.
 * The background has reduced opacity and uses a multiply blend mode to blend with underlying content.
 *
 * @returns {JSX.Element} A div element styled as a decorative background layer.
 */
export default function Background(): React.JSX.Element {
  return (
    <div
      className="absolute inset-0 z-0"
      style={{
        backgroundImage: `radial-gradient(circle at center, transparent 0%, #FF7112 100%)`,
        opacity: 0.3,
        mixBlendMode: "multiply",
      }}
    />
  );
}
