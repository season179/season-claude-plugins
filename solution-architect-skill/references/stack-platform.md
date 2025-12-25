# Platform Stack

## Contents
- WorkOS authentication
- PostHog analytics
- Playwright testing
- GitHub Actions CI/CD

## WorkOS Authentication

### Setup
```bash
npm install @workos-inc/node
```

### Auth Middleware
```typescript
import { WorkOS } from '@workos-inc/node'

const workos = new WorkOS(process.env.WORKOS_API_KEY)

const auth = createMiddleware(async (c, next) => {
  const token = getCookie(c, 'wos-session')
  if (!token) return c.redirect('/auth/login')
  
  try {
    const { user } = await workos.userManagement.loadSealedSession({
      sessionData: token,
      cookiePassword: c.env.WORKOS_COOKIE_PASSWORD
    })
    c.set('user', user)
    await next()
  } catch {
    return c.redirect('/auth/login')
  }
})
```

### Login Flow
```typescript
app.get('/auth/login', (c) => {
  const url = workos.userManagement.getAuthorizationUrl({
    provider: 'authkit',
    redirectUri: `${c.env.APP_URL}/auth/callback`,
    clientId: c.env.WORKOS_CLIENT_ID
  })
  return c.redirect(url)
})

app.get('/auth/callback', async (c) => {
  const { sealedSession } = await workos.userManagement.authenticateWithCode({
    code: c.req.query('code'),
    clientId: c.env.WORKOS_CLIENT_ID,
    session: { sealSession: true, cookiePassword: c.env.WORKOS_COOKIE_PASSWORD }
  })
  setCookie(c, 'wos-session', sealedSession, { httpOnly: true, secure: true })
  return c.redirect('/dashboard')
})
```

### SSO by Organization
```typescript
app.get('/auth/sso', async (c) => {
  const domain = c.req.query('email')?.split('@')[1]
  const org = await db.query.organizations.findFirst({
    where: eq(organizations.domain, domain)
  })
  
  if (!org?.workosOrgId) return c.redirect('/auth/login')
  
  const url = workos.userManagement.getAuthorizationUrl({
    organization: org.workosOrgId,
    redirectUri: `${c.env.APP_URL}/auth/callback`,
    clientId: c.env.WORKOS_CLIENT_ID
  })
  return c.redirect(url)
})
```

## PostHog Analytics

### Frontend Setup
```typescript
import posthog from 'posthog-js'

posthog.init(process.env.NEXT_PUBLIC_POSTHOG_KEY, {
  api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST
})

// Track events
posthog.capture('order_completed', { order_id: order.id, total: order.total })

// Identify users
posthog.identify(user.id, { email: user.email, plan: user.plan })

// Groups (B2B)
posthog.group('company', org.id, { name: org.name })
```

### Feature Flags
```typescript
// Frontend
import { useFeatureFlagEnabled } from 'posthog-js/react'

const showNewUI = useFeatureFlagEnabled('new-dashboard')

// Backend
import { PostHog } from 'posthog-node'

const posthog = new PostHog(process.env.POSTHOG_API_KEY)
const enabled = await posthog.isFeatureEnabled('new-feature', userId)
```

## Playwright Testing

### Config
```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile', use: { ...devices['iPhone 14'] } }
  ]
})
```

### Page Object Model
```typescript
// tests/pages/login.page.ts
export class LoginPage {
  constructor(private page: Page) {}
  
  readonly email = this.page.getByTestId('email-input')
  readonly password = this.page.getByTestId('password-input')
  readonly submit = this.page.getByTestId('login-button')
  
  async login(email: string, password: string) {
    await this.email.fill(email)
    await this.password.fill(password)
    await this.submit.click()
  }
}
```

### Tests
```typescript
import { test, expect } from '@playwright/test'
import { LoginPage } from './pages/login.page'

test('login works', async ({ page }) => {
  const login = new LoginPage(page)
  await page.goto('/login')
  await login.login('test@example.com', 'password')
  await expect(page).toHaveURL('/dashboard')
})
```

## GitHub Actions CI/CD

### Basic Deploy
```yaml
name: Deploy
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm test
      
      - name: Deploy
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          command: deploy
```

### Multi-Environment
```yaml
jobs:
  deploy-preview:
    if: github.event_name == 'pull_request'
    steps:
      - uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          command: deploy --env preview

  deploy-production:
    if: github.ref == 'refs/heads/main'
    environment: production
    steps:
      - name: Apply Migrations
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          command: d1 migrations apply my-database --remote
      
      - name: Deploy
        uses: cloudflare/wrangler-action@v3
        with:
          apiToken: ${{ secrets.CF_API_TOKEN }}
          command: deploy
```

### E2E in CI
```yaml
e2e:
  needs: deploy-preview
  steps:
    - run: npx playwright install --with-deps
    - run: npx playwright test
      env:
        BASE_URL: ${{ needs.deploy-preview.outputs.url }}
    - uses: actions/upload-artifact@v4
      if: failure()
      with:
        name: playwright-report
        path: playwright-report/
```
