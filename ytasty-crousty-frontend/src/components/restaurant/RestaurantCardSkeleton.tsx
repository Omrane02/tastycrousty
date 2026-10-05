import { Card, CardContent, Skeleton, Stack } from "@mui/material";

export function RestaurantCardSkeleton() {
  return (
    <Card aria-hidden>
      <Skeleton variant="rectangular" height={112} />
      <CardContent>
        <Skeleton width="70%" height={34} />
        <Skeleton width="35%" />
        <Stack spacing={1.5} sx={{ mt: 2.5 }}>
          <Skeleton variant="rounded" height={38} />
          <Skeleton variant="rounded" height={38} />
          <Skeleton variant="rounded" height={38} />
        </Stack>
        <Skeleton variant="rounded" height={46} sx={{ mt: 3, borderRadius: "999px" }} />
      </CardContent>
    </Card>
  );
}