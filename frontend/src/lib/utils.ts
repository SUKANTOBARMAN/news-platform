/**
 * ছোট, পুনর্ব্যবহারযোগ্য হেল্পার ফাংশন -- ক্লাসনেম মার্জ, ফরম্যাটিং, স্লাগ জেনারেশন ইত্যাদি।
 * (Poribar Health frontend-এর lib/utils.ts কনভেনশন অনুসরণ করে)
 *
 * STUB -- এখানে এখনো কোনো ইমপ্লিমেন্টেশন নেই।
 */

export function formatDate(iso: string): string {
  // TODO: Intl.DateTimeFormat দিয়ে বাংলা/ইংরেজি লোকেল-সচেতন ফরম্যাট করো
  return new Date(iso).toLocaleDateString();
}

export function truncate(text: string, maxLength: number): string {
  return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
}
