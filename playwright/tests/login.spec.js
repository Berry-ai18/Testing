import { test, expect } from '@playwright/test'

test.describe('Login', () => {
    test('Login with valid credentials', async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.fill('#user-name', 'standard_user')
        await page.fill('#password', 'secret_sauce')
        await page.click('[data-test="login-button"]')
        await expect(page).toHaveURL('https://www.saucedemo.com/inventory.html')
    })

    test('Login with wrong password', async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.fill('#user-name', 'standard_user')
        await page.fill('#password', 'wrongpassxdddd')
        await page.click('[data-test="login-button"]')
        await expect(page.locator('[data-test="error"]')).toBeVisible()
    })

    test('Login with no credentials at all', async ({ page }) => {
        await page.goto('https://www.saucedemo.com/')
        await page.click('[data-test="login-button"]')
        await expect(page.locator('[data-test="error"]')).toBeVisible()
    })
})