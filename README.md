## $5 Tech Unlocked 2021!
[Buy and download this Book for only $5 on PacktPub.com](https://www.packtpub.com/product/microservice-patterns-and-best-practices/9781788474030)
-----
*The $5 campaign         runs from __December 15th 2020__ to __January 13th 2021.__*

# Microservice Patterns and Best Practices
This is the code repository for [Microservice Patterns and Best Practices](https://www.packtpub.com/application-development/microservice-patterns-and-best-practices?utm_source=github&utm_medium=repository&utm_campaign=9781788474030), published by [Packt](https://www.packtpub.com/?utm_source=github). It contains all the supporting project files necessary to work through the book from start to finish.
## About the Book
Microservices are a hot trend in the development world right now. Many enterprises have adopted this approach to achieve agility and the continuous delivery of applications to gain a competitive advantage. This book will take you through the different design patterns at different stages of the microservice application development process, along with best practices.
## Instructions and Navigation
All of the code is organized into folders. Each folder starts with a number followed by the application name. For example, Chapter02.

Chapters 01, 02, 07, 08, and 09 don't have codes.
The remaining codes are placed in their respective chapter folders.

The code will look like the following:
```
class TestDevelopmentConfig(TestCase):
     
       def create_app(self):
             app.config.from_object('config.DevelopmentConfig')
             return app
       def test_app_is_development(self):
             self.assertTrue(app.config['DEBUG'] is True)
```

Having some knowledge of OOP and package structure in Go (golang) will make reading this book more interesting.

## Related Products
* [Hands-On Microservices with Kotlin](https://www.packtpub.com/web-development/microservices-kotlin?utm_source=github&utm_medium=repository&utm_campaign=9781788471459)

* [Building Microservices with .NET Core 2.0 - Second Edition](https://www.packtpub.com/application-development/building-microservices-net-core-20-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781788393331)

* [Mastering Microservices with Java 9 - Second Edition](https://www.packtpub.com/application-development/mastering-microservices-java-9-second-edition?utm_source=github&utm_medium=repository&utm_campaign=9781787281448)

### Suggestions and Feedback
[Click here](https://docs.google.com/forms/d/e/1FAIpQLSe5qwunkGf6PUvzPirPDtuy1Du5Rlzew23UBp2S-P3wB-GcwQ/viewform) if you have any feedback or suggestions.
