"""
Test Data Generator for Faberwork Test Automation
Uses Faker to generate realistic test data
"""

from faker import Faker
from typing import Dict, List
from loguru import logger


class TestDataGenerator:
    """Generate realistic test data using Faker"""

    def __init__(self, locale: str = 'en_US'):
        """
        Initialize Faker with specified locale

        Args:
            locale: Locale for generated data (default: en_US)
        """
        self.fake = Faker(locale)
        logger.debug(f"TestDataGenerator initialized with locale: {locale}")

    def generate_user_data(self) -> Dict[str, str]:
        """
        Generate user data for form submissions

        Returns:
            dict: User data including name, email, company, phone
        """
        data = {
            'name': self.fake.name(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': self.fake.email(),
            'company': self.fake.company(),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'city': self.fake.city(),
            'state': self.fake.state(),
            'zip_code': self.fake.zipcode(),
            'country': self.fake.country(),
        }
        logger.debug(f"Generated user data: {data.get('name')}")
        return data

    def generate_consultation_form_data(self) -> Dict[str, str]:
        """
        Generate data specifically for consultation form

        Returns:
            dict: Consultation form data
        """
        data = {
            'name': self.fake.name(),
            'email': self.fake.email(),
            'company': self.fake.company(),
            'phone': self.fake.phone_number(),
            'message': self.fake.text(max_nb_chars=200),
        }
        logger.debug("Generated consultation form data")
        return data

    def generate_contact_form_data(self) -> Dict[str, str]:
        """
        Generate data for contact form

        Returns:
            dict: Contact form data
        """
        data = {
            'name': self.fake.name(),
            'email': self.fake.email(),
            'subject': self.fake.sentence(nb_words=6),
            'message': self.fake.paragraph(nb_sentences=5),
            'phone': self.fake.phone_number(),
        }
        logger.debug("Generated contact form data")
        return data

    def generate_newsletter_email(self) -> str:
        """
        Generate email for newsletter subscription

        Returns:
            str: Email address
        """
        email = self.fake.email()
        logger.debug(f"Generated newsletter email: {email}")
        return email

    def generate_invalid_emails(self, count: int = 5) -> List[str]:
        """
        Generate invalid email formats for testing

        Args:
            count: Number of invalid emails to generate

        Returns:
            list: List of invalid email strings
        """
        invalid_emails = [
            'invalid',
            '@example.com',
            'test@',
            'test..email@example.com',
            'test email@example.com',
            'test@example',
            'test@.com',
            '@',
            'test@example..com',
            'test@@example.com',
        ]
        return invalid_emails[:count]

    def generate_search_queries(self) -> List[str]:
        """
        Generate search query terms

        Returns:
            list: List of search queries
        """
        queries = [
            'software development',
            'mobile app',
            'AI solutions',
            'database',
            'testing',
            'automation',
            self.fake.word(),
            self.fake.bs(),
        ]
        logger.debug("Generated search queries")
        return queries

    def generate_chatbot_messages(self) -> List[str]:
        """
        Generate chatbot test messages

        Returns:
            list: List of chatbot messages
        """
        messages = [
            'Hello',
            'I need help with my project',
            'What services do you offer?',
            'Can you help me with software development?',
            'I want to know about pricing',
            self.fake.sentence(),
        ]
        logger.debug("Generated chatbot messages")
        return messages

    def generate_company_data(self) -> Dict[str, str]:
        """
        Generate company information

        Returns:
            dict: Company data
        """
        data = {
            'company_name': self.fake.company(),
            'industry': self.fake.bs(),
            'website': self.fake.url(),
            'employees': str(self.fake.random_int(min=10, max=10000)),
            'revenue': f"${self.fake.random_int(min=100000, max=10000000)}",
            'description': self.fake.catch_phrase(),
        }
        logger.debug(f"Generated company data: {data.get('company_name')}")
        return data

    def generate_text(self, sentences: int = 3) -> str:
        """
        Generate random text

        Args:
            sentences: Number of sentences to generate

        Returns:
            str: Generated text
        """
        text = self.fake.paragraph(nb_sentences=sentences)
        logger.debug(f"Generated text with {sentences} sentences")
        return text

    def generate_url(self) -> str:
        """
        Generate a fake URL

        Returns:
            str: URL
        """
        url = self.fake.url()
        logger.debug(f"Generated URL: {url}")
        return url

    def generate_date(self, pattern: str = "%Y-%m-%d") -> str:
        """
        Generate a date string

        Args:
            pattern: Date format pattern

        Returns:
            str: Formatted date string
        """
        date = self.fake.date(pattern=pattern)
        logger.debug(f"Generated date: {date}")
        return date

    def generate_file_name(self, extension: str = 'txt') -> str:
        """
        Generate a random file name

        Args:
            extension: File extension

        Returns:
            str: File name
        """
        filename = f"{self.fake.word()}_{self.fake.random_number(digits=4)}.{extension}"
        logger.debug(f"Generated filename: {filename}")
        return filename


# Create a default instance for easy importing
test_data_generator = TestDataGenerator()
