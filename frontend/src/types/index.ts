/**
 * Backend Pydantic schema-র সাথে মিলিয়ে TypeScript টাইপ রাখা হয় -- module-by-module
 * implementation-এর সময় backend/app/schemas/*.py বদলালে এখানেও মিলিয়ে বদলাতে হবে।
 *
 * নোট: বাকি সব মডিউলের জন্য আলাদা টাইপ ফাইল আগে থেকেই আছে এই ফোল্ডারে
 * (types/article.ts, types/billing.ts, ...) -- সেগুলো লেখা শেষ হলে এখান
 * থেকে re-export করলে `import { X } from "@/types"` সবজায়গায় কাজ করবে, যেমন:
 *   export * from "./article";
 *   export * from "./billing";
 */
export interface User {
  id: number;
  first_name: string;
  last_name: string;
  email: string | null;
  phone: string | null;
  is_journalist: boolean;
  preferred_locale: string;
  created_at: string;
}

export interface UserCreatePayload {
  first_name: string;
  last_name: string;
  email?: string;
  phone?: string;
  password: string;
}
