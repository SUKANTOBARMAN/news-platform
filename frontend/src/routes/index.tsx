/**
 * কেন্দ্রীয় route configuration -- App.tsx এখান থেকেই route element গুলো বসায়।
 * role-ভিত্তিক ফোল্ডার স্ট্রাকচারের সাথে মিলিয়ে route path সাজানো হয়েছে।
 *
 * STUB -- নিচে শুধু কাঠামো দেখানো হয়েছে, পেজ লেখা শেষ হলে import + Route
 * আনকমেন্ট করবে।
 */
// import { Route } from "react-router-dom"; // TODO: route যোগ করার সময় আনকমেন্ট করো

// import HomePage from "@/pages/Home";
// import NotFoundPage from "@/pages/NotFound";

// Public pages (role: public)
// import LoginPage from "@/pages/public/Login";
// import RegisterPage from "@/pages/public/Register";
// import ArticleDetailPage from "@/pages/public/ArticleDetail";
// import CategoryPage from "@/pages/public/CategoryPage";
// import SearchResultsPage from "@/pages/public/SearchResults";
// import PodcastDetailPage from "@/pages/public/PodcastDetail";
// import LiveEventPage from "@/pages/public/LiveEventPage";

// User pages (role: user, auth-protected)
// import ProfilePage from "@/pages/user/Profile";
// import BookmarksPage from "@/pages/user/Bookmarks";
// import SubscriptionPlansPage from "@/pages/user/SubscriptionPlans";
// import CheckoutPage from "@/pages/user/Checkout";

// Editorial pages (role: editorial, staff-only)
// import EditorialDashboardPage from "@/pages/editorial/EditorialDashboard";

// Admin pages (role: admin, staff-only)
// import AdminDashboardPage from "@/pages/admin/AdminDashboard";

/**
 * TODO: প্রতিটা পেজ লেখা শেষ হলে এখানে <Route> যোগ করো, তারপর App.tsx-এ
 * <AppRoutes /> হিসেবে ব্যবহার করো। protected route-এর জন্য (user/editorial/admin)
 * একটা RequireAuth wrapper component বানানো ভালো হবে (hooks/useAuth.ts-এর
 * token/role চেক করে)।
 */
export function AppRoutes() {
  return (
    <>
      {/* <Route path="/" element={<HomePage />} /> */}
      {/* <Route path="/login" element={<LoginPage />} /> */}
      {/* <Route path="/register" element={<RegisterPage />} /> */}
      {/* <Route path="/articles/:slug" element={<ArticleDetailPage />} /> */}
      {/* <Route path="/category/:slug" element={<CategoryPage />} /> */}
      {/* <Route path="/search" element={<SearchResultsPage />} /> */}

      {/* <Route path="/profile" element={<ProfilePage />} /> */}
      {/* <Route path="/bookmarks" element={<BookmarksPage />} /> */}
      {/* <Route path="/subscribe" element={<SubscriptionPlansPage />} /> */}
      {/* <Route path="/checkout" element={<CheckoutPage />} /> */}

      {/* <Route path="/editorial/*" element={<EditorialDashboardPage />} /> */}
      {/* <Route path="/admin/*" element={<AdminDashboardPage />} /> */}

      {/* <Route path="*" element={<NotFoundPage />} /> */}
    </>
  );
}
