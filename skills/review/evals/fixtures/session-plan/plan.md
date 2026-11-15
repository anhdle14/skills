# Move user sessions from Redis to Postgres

## Goal

Store web sessions in the existing `app` Postgres database instead of Redis, so we can retire the Redis cluster this quarter.
The migration has zero downtime.

## Steps

1. Create the `sessions` table with columns `id text primary key`, `user_id bigint`, `data jsonb`, and `created_at timestamptz`.
2. Shut down the Redis cluster to stop new session writes.
3. Copy every key from Redis into the `sessions` table with a one-off script.
4. Switch `SESSION_BACKEND` from `redis` to `postgres` and deploy.
5. Delete expired sessions once a month with a cron job.

## Validation

Check that login still works.

## Risks

None expected; Postgres is already in production.
