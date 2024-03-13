from django.contrib.auth import get_user_model
from django.http import Http404
from django.test import TestCase
from django.urls import reverse, reverse_lazy
from taggit.models import Tag

from blog.forms import CommentForm
from blog.models import Category, Comment, Post
from blog.views import PostDetailView

User = get_user_model()


class LikePostTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        cls.review = Post.objects.create(
            title='Test Review',
            body='Body of test review.'
        )

    def test_like_post_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('blog:like_post', kwargs={'pk': self.review.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.user, self.review.likes.all())

    def test_like_and_unlike_review_with_authenticated_user(self):
        self.client.force_login(self.user)

        # Like the review
        self.client.post(
            reverse('blog:like_post', kwargs={'pk': self.review.pk})
        )  # For like
        self.assertEqual(self.review.likes.count(), 1)
        self.assertIn(self.user, self.review.likes.all())

        # Unlike the review
        self.client.post(
            reverse('blog:like_post',
                    kwargs={'pk': self.review.pk})
        )
        self.assertEqual(self.review.likes.count(), 0)
        self.assertNotIn(self.user, self.review.likes.all())


class ReviewsPageTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            pub_date='2020-01-01',
            author=self.author1,
            body='The body of the sample post review',
            status='PUB'
        )
        self.post2 = Post.objects.create(
            title='Another Sample Post Review',
            slug='another-post-review',
            pub_date='2021-01-01',
            author=self.author1,
            body='The body of the another sample post review.',
            status='PUB'
        )
        self.post3 = Post.objects.create(
            title='Again Another Sample Post Review',
            slug='once-more-post-review',
            pub_date='2021-08-01',
            author=self.author1,
            body='The body of the third sample post review',
            status='PUB'
        )
        self.post4 = Post.objects.create(
            title='The last one',
            slug='the-last-test-post',
            pub_date='2023-01-01',
            author=self.author1,
            body='The body of the fourth sample post review.',
            status='PUB'
        )

    def test_home_page_returns_correct_response(self):
        response = self.client.get(reverse('blog:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_displays_added_posts(self):
        response = self.client.get(reverse('blog:home'))
        self.assertContains(response, self.post2.title)
        self.assertContains(response, self.post2.body)

    def test_pagination_displays(self):
        response = self.client.get(reverse('blog:home'))
        self.assertTrue(response.context['is_paginated'])
        self.assertIn('paginator', response.context)


class PostDetailViewTestCase(TestCase):
    def setUp(self):
        self.author1 = User.objects.create(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

        self.post1 = Post.objects.create(
            title='Sample Post Review',
            slug='sample-post-review',
            pub_date='2020-01-01',
            author=self.author1,
            body='The body of the Sample Post Review.',
            status='PUB',
        )

        self.tag1 = Tag.objects.create(name='test_tag_1')
        self.tag2 = Tag.objects.create(name='test_tag_2')

        self.post1.tags.add(self.tag1)
        self.post1.tags.add(self.tag2)

    def test_get_success_url_with_invalid_object(self):
        view = PostDetailView()
        view.object = None  # Simulating the absence of the Post instance

        with self.assertRaises(Http404) as context:
            view.get_success_url()

        self.assertEqual(str(context.exception), "Post not found.")

    def test_post_detail_returns_correct_response(self):
        url = self.post1.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_template_contains_body_and_title(self):
        url = self.post1.get_absolute_url()
        response = self.client.get(url)
        self.assertContains(response, self.post1.body)
        self.assertContains(response, self.post1.title)

    def test_post_likes_with_zero_likes(self):
        response = self.client.get(self.post1.get_absolute_url())
        post_likes_from_context = response.context['post_likes']
        expected_post_likes = '0 Likes'
        self.assertEqual(post_likes_from_context, expected_post_likes)

    def test_post_likes_with_one_like(self):
        self.client.force_login(self.author1)
        self.client.post(reverse('blog:like_post', kwargs={'pk': self.post1.pk}))
        response = self.client.get(self.post1.get_absolute_url())
        post_likes_from_context = response.context['post_likes']
        expected_post_likes = '1 Like'
        self.assertEqual(post_likes_from_context, expected_post_likes)

    def test_get_related_posts_with_zero_related_posts(self):
        response = self.client.get(self.post1.get_absolute_url())
        related_posts_of_post_1 = response.context['related_posts']
        amount_of_related_posts_for_post1 = len(related_posts_of_post_1)
        expected_amount_of_related_posts = 0
        self.assertEqual(
            amount_of_related_posts_for_post1,
            expected_amount_of_related_posts
        )

    def test_get_related_posts_with_one_related_post(self):
        related_post1 = Post.objects.create(
            title='Related Post 1',
            body='Body of Related Post 1'
        )
        related_post1.tags.add(self.tag1)

        response = self.client.get(self.post1.get_absolute_url())
        related_posts_of_post_1 = response.context['related_posts']
        amount_of_related_posts_for_post1 = len(related_posts_of_post_1)
        expected_amount_of_related_posts = 1
        self.assertEqual(
            amount_of_related_posts_for_post1,
            expected_amount_of_related_posts
        )

    def test_get_related_posts_with_four_related_posts(self):
        related_post1 = Post.objects.create(
            title='Related Post 1',
            body='Body of Related Post 1'
        )
        related_post2 = Post.objects.create(
            title='Related Post 2',
            body='Body of Related Post 2'
        )
        related_post3 = Post.objects.create(
            title='Related Post 3',
            body='Body of Related Post 3'
        )
        related_post4 = Post.objects.create(
            title='Related Post 4',
            body='Body of Related Post 4'
        )
        related_post1.tags.add(self.tag1)
        related_post2.tags.add(self.tag2)
        related_post3.tags.add(self.tag1)
        related_post4.tags.add(self.tag1)
        related_post4.tags.add(self.tag2)

        response = self.client.get(self.post1.get_absolute_url())
        related_posts_of_post1 = list(response.context['related_posts'])
        amount_of_related_posts_for_post1 = len(related_posts_of_post1)
        expected_amount_of_related_posts = 3
        self.assertEqual(
            amount_of_related_posts_for_post1,
            expected_amount_of_related_posts
        )


class PostDetailViewCommentTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create(
            username='author',
            password='test_password',
        )
        self.post = Post.objects.create(
            title='Sample Post Review',
            pub_date='2020-01-01',
            author=self.author,
            body='The body of the Sample Post Review.',
            status='PUB',
        )
        self.comment_data_authenticated_user = {
            'body': 'This is a random comment written by an authenticated user.'
        }
        self.comment_data_unauthenticated_user = {
            'body': 'This is a random comment written by an unauthenticated user.'
        }

    def test_comment_form_displayed(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_user_can_add_comment(self):
        self.client.force_login(self.author)
        response = self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_authenticated_user
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_fields_added_correctly_for_authenticated_user(self):
        self.client.force_login(self.author)
        self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_authenticated_user
        )
        new_comment = Comment.objects.last()

        self.assertEqual(new_comment.post, self.post)
        self.assertFalse(new_comment.active)
        self.assertIsNone(new_comment.unlogged_user)
        self.assertEqual(new_comment.logged_user, self.author)

    def test_unauthenticated_user_can_add_comment(self):
        self.client.logout()
        response = self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_unauthenticated_user
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 1)

    def test_comment_fields_added_correctly_for_unauthenticated_user(self):
        self.client.logout()
        self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_unauthenticated_user
        )
        new_comment = Comment.objects.last()

        self.assertEqual(new_comment.post, self.post)
        self.assertFalse(new_comment.active)
        self.assertIsNone(new_comment.logged_user)
        self.assertEqual(new_comment.unlogged_user, 'guest')

    def test_display_success_message_after_comment_addition(self):
        response = self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_authenticated_user,
            follow=True
        )
        expected_success_message_excerpt = 'comment successfully' \
            ' <strong>submitted</strong>'
        messages = [str(message).lower() for message in response.context['messages']]
        self.assertTrue(
            any(expected_success_message_excerpt in message for message in messages)
        )

    def test_comment_success_message_for_superuser(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='test_superuser',
            email='superuser@mail.com'
        )
        self.client.force_login(superuser)
        response = self.client.post(
            self.post.get_absolute_url(),
            data=self.comment_data_authenticated_user,
            follow=True
        )
        expected_success_message_excerpt = 'comment successfully <strong>added</strong>'
        messages = [str(message).lower() for message in response.context['messages']]
        self.assertTrue(
            any(expected_success_message_excerpt in message for message in messages)
        )

    def test_comment_without_parent_response_to_field(self):
        comment_without_parent = Comment.objects.create(
            post=self.post,
            body=self.comment_data_authenticated_user
        )
        self.assertIsNone(comment_without_parent.response_to)

    def test_comment_with_parent_response_to_field(self):
        self.client.force_login(self.author)
        parent_comment = Comment.objects.create(
            post=self.post,
            body="Parent comment body",
            logged_user=self.author,
            active=True
        )
        child_comment_data = {
            'body': 'Child comment body',
            'comment_parent_id': parent_comment.id
        }
        response = self.client.post(
            self.post.get_absolute_url(),
            data=child_comment_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        child_comment = Comment.objects.all()[0]
        self.assertEqual(child_comment.response_to, parent_comment)

    def test_invalid_comment_form(self):
        self.client.force_login(self.author)
        invalid_comment_data = {'body': ''}
        response = self.client.post(
            self.post.get_absolute_url(),
            data=invalid_comment_data,
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 0)

    def test_edit_comment_successfully(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='test_superuser',
            email='superuser@mail.com'
        )
        self.client.force_login(superuser)
        comment = Comment.objects.create(
            logged_user=superuser,
            post=self.post,
            body=self.comment_data_authenticated_user,
            active=True
        )
        self.assertTrue(Comment.objects.filter(pk=comment.id).exists())

        comment_form_data = {
            'body': 'Edited comment body.',
            'editing_comment_id': comment.id
        }
        comment_form = CommentForm(data=comment_form_data)
        self.assertTrue(comment_form.is_valid())

        self.client.post(
            self.post.get_absolute_url(),
            comment_form_data,
            follow=True
        )
        edited_comment = Comment.objects.get(pk=comment.id)
        self.assertEqual(edited_comment.body, comment_form_data['body'])


class CommentDeleteViewTestCase(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username='admin',
            password='admin_password',
        )
        self.post = Post.objects.create(
            title='Sample Post Review',
            author=self.admin,
            body='The body of the Sample Post Review.',
            status='PUB',
        )
        self.comment_to_delete = Comment.objects.create(
            post=self.post,
            body='Body comment',
            active=True
        )

    def test_comment_delete_view(self):
        self.client.force_login(self.admin)
        delete_url = reverse(
            'blog:delete_comment', kwargs={'pk': self.comment_to_delete.id}
        )
        response = self.client.delete(delete_url)
        self.assertEqual(response.status_code, 303)
        self.assertRaises(
            Comment.DoesNotExist,
            Comment.objects.get,
            pk=self.comment_to_delete.id
        )


class PostCreateTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
            username='random',
            password='testpassword',
            bio='This is the random author for testing.'
        )

    def test_unlogged_user_redirect_to_login(self):
        response = self.client.get(reverse('blog:create_review'))
        self.assertEqual(response.status_code, 302)
        expected_url = (
            reverse('accounts:login') +
            '?next=' +
            reverse('blog:create_review')
        )
        self.assertRedirects(response, expected_url)

    def test_logged_user_without_permission_returns_403_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse_lazy('blog:create_review'))
        self.assertEqual(response.status_code, 403)


class PostCreateWithPermissionTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='admin',
            password='admin-password'
        )
        self.client.force_login(self.adminuser)

        self.first_review = {
            'title': 'New Review',
            'body': 'The body of the new review',
            'status': 'PUB'
        }

    def test_display_add_review_success(self):
        self.assertTrue(self.adminuser.has_perm('blog.add_post'))
        response = self.client.get(reverse_lazy('blog:create_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/review_create.html')

    def test_successful_post_creation_redirect(self):
        response = self.client.post(
            reverse_lazy('blog:create_review'),
            data=self.first_review
        )
        expected_url_after_post = '/blog/new-review/'  # slug created automatically
        self.assertRedirects(response, expected_url_after_post)

    def test_successful_post_adding_to_database(self):
        second_review = {
            'title': 'Second Review',
            'body': 'The body of the new review',
            'status': 'PUB'

        }
        self.client.post(
            reverse_lazy('blog:create_review'), data=self.first_review
        )
        self.client.post(
            reverse_lazy('blog:create_review'), data=second_review
        )

        posts_amount = Post.objects.count()
        self.assertEqual(posts_amount, 2)

        # Check if the author is assigned to the posts
        first_post = Post.objects.get(title='New Review')
        author_of_first_post = first_post.author
        self.assertEqual(author_of_first_post, self.adminuser)


class PostUpdateTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            password='xyz',
            email='author@mail.com',
            is_author=True
        )
        self.second_author = User.objects.create_user(
            username='second_author',
            password='xyz',
            email='second_author@mail.com',
            is_author=True
        )
        self.superuser = User.objects.create_superuser(
            username='admin',
            password='pass',
            email='admin@mail.com'
        )
        self.category = Category.objects.create(
            name='Peanut Butter'
        )
        self.review = Post.objects.create(
            title='Protein Bar Review',
            body='This is a review of Protein Bar. I really liked it.',
            author=self.author,
            category=self.category,
        )
        self.staff = User.objects.create_user(
            username='staff',
            password='abc',
            email='staff@mail.com',
            is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username='normal_user',
            password='abc',
            email='normal_user@mail.com'
        )

    def test_author_can_access_update_view(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse(
                'blog:update_review',
                kwargs={'pk': self.review.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/review_update.html')

    def test_superuser_can_access_update_view(self):
        self.client.force_login(self.superuser)
        response = self.client.get(
            reverse(
                'blog:update_review',
                kwargs={'pk': self.review.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/review_update.html')

    def test_staff_can_access_update_view(self):
        self.client.force_login(self.staff)
        response = self.client.get(
            reverse(
                'blog:update_review',
                kwargs={'pk': self.review.pk}
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/review_update.html')

    def test_normal_user_cannot_access_update_view(self):
        self.client.force_login(self.normal_user)
        response = self.client.get(
            reverse('blog:update_review', kwargs={'pk': self.review.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_other_author_cannot_update_post(self):
        self.client.force_login(self.second_author)
        response = self.client.get(
            reverse('blog:update_review', kwargs={'pk': self.review.pk})
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_not_logged_user_redirect_login_page(self):
        self.client.logout()
        response = self.client.get(
            reverse('blog:update_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertTemplateUsed(response, 'registration/login.html')


class PostDeleteTestCase(TestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            password='xyz',
            is_author=True
        )
        self.review = Post.objects.create(
            title='Vegan Chocolate Review',
            body='This is a review of Vegan Chocolate. Not tasty.',
            author=self.author,
        )

    def test_author_can_access_delete_view(self):
        self.client.force_login(self.author)
        response = self.client.get(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/review_delete.html')

    def test_staff_can_access_delete_view(self):
        User.objects.create_user(
            username='admin',
            password='abc',
            email='admin@mail.com',
            is_staff=True
        )
        self.client.force_login(self.author)
        response = self.client.get(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/review_delete.html')

    def test_superuser_can_access_delete_view(self):
        superuser = User.objects.create_superuser(
            username='superuser',
            password='abc',
            email='superuser@mail.com'
        )
        self.client.force_login(superuser)
        response = self.client.get(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('blog/review_delete.html')

    def test_other_author_cannot_delete_post(self):
        other_author = User.objects.create_user(
            username='other_author',
            password='xyz',
            email='other_author@mail.com',
            is_author=True
        )
        self.client.force_login(other_author)
        response = self.client.get(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, '403.html')

    def test_random_user_redirect_login_page(self):
        self.client.logout()
        response = self.client.get(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_get_success_message(self):
        self.client.force_login(self.author)
        response = self.client.post(
            reverse('blog:delete_review', kwargs={'pk': self.review.pk}),
            follow=True
        )
        self.assertTemplateUsed(response, 'blog/home.html')

        success_messages = [str(message) for message in response.context['messages']]
        expected_message = f"Post <strong>{self.review.title}</strong>" \
            " deleted successfully."
        self.assertEqual(success_messages[0], expected_message)


class PostStatusTestCase(TestCase):
    def setUp(self):
        self.adminuser = User.objects.create_superuser(
            username='author',
            password='author-password'
        )
        self.client.force_login(self.adminuser)

    def check_post_visibility(self, title, body, status, should_appear):
        post = Post.objects.create(title=title, body=body, status=status)
        homepage = self.client.get(reverse('blog:home'))

        if should_appear:
            self.assertContains(homepage, post)
        else:
            self.assertNotContains(homepage, post)

    def check_post_not_published(self, title, body, status, slug):
        response = self.client.post(
            reverse('blog:create_review'),
            data={'title': title, 'body': body, 'status': status}
        )
        self.assertRedirects(response, '/blog/')
        response = self.client.get(
            reverse('blog:detail_review', kwargs={'slug': slug})
        )
        self.assertEqual(response.status_code, 404)

    def check_post_create_and_save(self, title, body, status):
        post_data = {'title': title, 'body': body, 'status': status}
        self.client.post(reverse('blog:create_review'), post_data)
        post_amount = Post.objects.count()
        self.assertEqual(post_amount, 1)

    # Start testing
    def test_post_to_publish_should_not_appear_on_homepage(self):
        self.check_post_visibility(
            title='The first to-publish review',
            body='This is the body of a two-publish review.',
            status='TO_PUB',
            should_appear=False
        )

    def test_post_to_publish_should_not_be_published(self):
        self.check_post_not_published(
            title='The second to-publish review',
            body='This is the body of a second two-publish review.',
            status='TO_PUB',
            slug='the-second-to-publish-review'
        )

    def test_post_to_publish_create_and_save(self):
        self.check_post_create_and_save(
            title='The third to-publish review',
            body='This is the body of a second two-publish review.',
            status='TO_PUB',
        )

    def test_post_published_should_appear_on_homepage(self):
        self.check_post_visibility(
            title='The new review',
            body='This is the body of the new review.',
            status='PUB',
            should_appear=True
        )

    def test_post_published_should_be_published(self):
        post_data = {
            'title': 'The new review',
            'body': 'This is the body of the new review.',
            'status': 'PUB',
            'slug': 'the-new-review'
        }
        response = self.client.post(reverse('blog:create_review'), post_data)
        self.assertRedirects(
            response,
            reverse('blog:detail_review', kwargs={'slug': post_data['slug']})
        )

    def test_post_published_create_and_save(self):
        self.check_post_create_and_save(
            title='The new review',
            body='This is the body of the new review.',
            status='PUB'
        )

    def test_post_draft_should_not_appear_on_homepage(self):
        self.check_post_visibility(
            title='The first draft review',
            body='This is the body of a draft review.',
            status='DRAFT',
            should_appear=False
        )

    def test_post_draft_should_not_be_published(self):
        self.check_post_not_published(
            title='The second draft review',
            body='This is the body of a second draft review.',
            status='DRAFT',
            slug='the-second-draft-review'
        )

    def test_post_draft_create_and_save(self):
        self.check_post_create_and_save(
            title='The second draft review',
            body='This is the body of a second draft review.',
            status='DRAFT',
        )

    def test_popular_posts_in_context(self):
        response = self.client.get(reverse('blog:home'))
        self.assertIn('popular_posts', response.context)
        self.assertIsInstance(response.context['popular_posts'], list)
        self.assertLessEqual(len(response.context['popular_posts']), 5)
        self.assertGreaterEqual(len(response.context['popular_posts']), 0)

    def test_recent_comments_in_context(self):
        response = self.client.get(reverse('blog:home'))
        self.assertIn('recent_comments', response.context)
        self.assertIsInstance(response.context['recent_comments'], list)
        self.assertLessEqual(len(response.context['recent_comments']), 3)
        self.assertGreaterEqual(len(response.context['recent_comments']), 0)


class TagsListTestCase(TestCase):
    def test_successful_tags_list_displaying(self):
        response = self.client.get(reverse('blog:tags'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tags.html')


class TaggedPostsListTestCase(TestCase):
    def setUp(self):
        self.tag_bars = Tag.objects.create(
            name='bars'
        )
        self.tag_drinks = Tag.objects.create(
            name='drinks'
        )
        self.post1 = Post.objects.create(
            title='Chocolate bar',
            body='This is the body of the chocolate bar review.',
            status='PUB',
        )
        self.post2 = Post.objects.create(
            title='Protein bar',
            body='This is the body of the protein bar review.',
            status='TO_PUB',
        )
        self.post3 = Post.objects.create(
            title='White chocolate bar',
            body='This is the body of the white chocolate bar review.',
            status='DRAFT',
        )
        self.post4 = Post.objects.create(
            title='Energydrink Zero',
            body='This is the body of the Energydrink Zero',
            status='PUB',
        )
        self.post5 = Post.objects.create(
            title='Fruit Bar',
            body='This is the body of the Fruit Zero',
            status='PUB',
        )

        posts = [self.post1, self.post2, self.post3, self.post5]
        for post in posts:
            post.tags.add(self.tag_bars)
        self.post4.tags.add(self.tag_drinks)

    def test_tag_page_success(self):
        tag_slug = self.tag_bars.slug
        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': tag_slug})
        )
        self.assertEqual(response.status_code, 200)

    def test_tag_page_uses_home_template(self):
        tag_slug = self.tag_bars.slug
        self.client.get(
            reverse('blog:tag', kwargs={'slug': tag_slug})
        )
        self.assertTemplateUsed('blog/home.html')

    def test_filtering_tagged_posts(self):
        tag_slug = self.tag_bars.slug

        response = self.client.get(
            reverse('blog:tag', kwargs={'slug': tag_slug})
        )
        filtered_tagged_posts = [self.post1, self.post5]

        self.assertQuerysetEqual(
            response.context['posts'],
            filtered_tagged_posts
        )


class CategoryViewsTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='masła orzechowe'
        )
        self.post1 = Post.objects.create(
            title='Chocolate bar',
            body='This is the body of the chocolate bar review.',
            status='PUB',
        )
        self.post2 = Post.objects.create(
            title='Peanut Butter Crunchy',
            category=self.category,
            body='This is the body of the peanut butter crunchy review.',
            status='PUB',
        )
        self.post3 = Post.objects.create(
            title='Peanut Butter with white chocolate',
            category=self.category,
            body='This is the body of the peanut butter with white chocolate review.',
            status='DRAFT',
        )

    def test_successfull_category_page_load(self):
        response = self.client.get(
            reverse(
                'blog:category',
                kwargs={'category_name': self.category.slug}
            ))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/home.html')

    def test_display_published_post_from_proper_category(self):
        category_peanut_butter = self.category.slug
        response = self.client.get(
            reverse(
                'blog:category',
                kwargs={'category_name': category_peanut_butter}
                ))

        expected_posts = [self.post2]
        self.assertQuerysetEqual(
            response.context['posts'],
            expected_posts
        )
