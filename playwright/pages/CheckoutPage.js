class CheckoutPage {
    constructor(page){
        this.page = page
        this.firstNameInput = page.locator('[data-test="firstName"]')
        this.lastNameInput = page.locator('[data-test="lastName"]')
        this.postalCodeInput = page.locator('[data-test="postalCode"]')
        this.continueInput = page.locator('[data-test="continue"]')
        this.finishInput = page.locator('[data-test="finish"]')
        this.completeHeder = page.locator('[data-test="complete-header"]')
        this.errorButton = page.locator('[data-test="error-button"]')
    }

    async fillCheckoutForm(username, password, postal_code = '') {
        await this.firstNameInput.fill(username)
        await this.lastNameInput.fill(password)
        await this.postalCodeInput.fill(postal_code)
    }

    async continue(){
        await this.continueInput.click()
    }
    
    async finish(){
        await this.finishInput.click()
    }
}

export default CheckoutPage