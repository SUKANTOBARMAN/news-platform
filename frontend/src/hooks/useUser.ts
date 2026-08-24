import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { createUser, getUser } from "@/api/users";
import type { UserCreatePayload } from "@/types";

export function useUser(id: number) {
  return useQuery({
    queryKey: ["user", id],
    queryFn: () => getUser(id),
    enabled: !!id,
  });
}

export function useCreateUser() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: UserCreatePayload) => createUser(payload),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user"] });
    },
  });
}
