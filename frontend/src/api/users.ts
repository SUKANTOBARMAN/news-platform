import { apiClient } from "@/api/client";
import type { User, UserCreatePayload } from "@/types";

/**
 * Module 2 (Identity & Access Management)-এর সাথে সম্পর্কিত API কল।
 * module-by-module implementation-এর সময় প্রতিটা মডিউলের জন্য এরকম একটা ফাইল
 * বানাবে (articles.ts, categories.ts, ...) -- react-query hook গুলো এখান
 * থেকেই ফাংশন import করবে।
 */
export async function createUser(payload: UserCreatePayload): Promise<User> {
  const { data } = await apiClient.post<User>("/users/", payload);
  return data;
}

export async function getUser(id: number): Promise<User> {
  const { data } = await apiClient.get<User>(`/users/${id}`);
  return data;
}
