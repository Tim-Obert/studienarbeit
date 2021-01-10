import Dotenv from "dotenv-webpack"


module.exports = {
    configureWebpack: {
        plugins: [
            new Dotenv()
        ]
    }
}
