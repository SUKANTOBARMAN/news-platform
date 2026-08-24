import { Outlet } from "react-router-dom";

/**
 * সব পেজের জন্য কমন লেআউট (header/footer/nav) -- module-by-module
 * implementation-এর সময় এখানে Header, Footer, navigation menu যোগ করবে।
 */
export default function AppLayout() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <h1>News Platform</h1>
      </header>
      <main className="app-content">
        <Outlet />
      </main>
      <footer className="app-footer">
        <p>&copy; {new Date().getFullYear()} News Platform</p>
      </footer>
    </div>
  );
}
