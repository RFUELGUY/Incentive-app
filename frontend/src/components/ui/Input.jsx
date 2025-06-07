export default function Input({ label, ...props }) {
  return (
    <div className="mb-4">
      {label && <label className="block mb-1 text-sm font-medium">{label}</label>}
      <input
        {...props}
        className="w-full px-3 py-2 border rounded-md shadow-sm focus:outline-none focus:ring"
      />
    </div>
  );
}
