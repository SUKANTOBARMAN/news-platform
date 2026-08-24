import { Route, Routes } from "react-router-dom";

import AppLayout from "@/layouts/AppLayout";
import HomePage from "@/pages/Home";
import NotFoundPage from "@/pages/NotFound";
import { AppRoutes } from "@/routes";

/**
 * এখানে শুধু root layout ও ফ্ল্যাট (role-নিরপেক্ষ) পেজগুলো (Home, NotFound)
 * সরাসরি বসানো আছে। role-ভিত্তিক পেজের route (public/, user/, editorial/,
 * admin/) routes/index.tsx-এ <AppRoutes /> এর ভেতরে যোগ করবে -- সেখানে
 * এখনো সব কমেন্ট করা আছে, পেজ লেখা শেষ হলে আনকমেন্ট করবে।
 */
function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<HomePage />} />
        {AppRoutes()}
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}

export default App;
