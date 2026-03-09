"""Fixtures for search tests.

Provides a populated test database with 15+ sample papers covering
multiple categories, date ranges, and varied text content for
integration testing of the search service.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from arxiv_mcp.config import get_settings
from arxiv_mcp.db.models import Base, Paper
from tests.conftest import (
    TSVECTOR_FUNCTION_SQL,
    TSVECTOR_DROP_TRIGGER_SQL,
    TSVECTOR_CREATE_TRIGGER_SQL,
    sample_paper_data,
)


# --- Sample paper dataset ---

SAMPLE_PAPERS = [
    # cs.CL papers (NLP / computational linguistics)
    sample_paper_data(
        arxiv_id="2301.00001",
        title="Attention Is All You Need",
        authors_text="Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit",
        abstract=(
            "The dominant sequence transduction models are based on complex recurrent "
            "or convolutional neural networks that include an encoder and a decoder. "
            "We propose a new simple network architecture, the Transformer, based solely "
            "on attention mechanisms, dispensing with recurrence and convolutions entirely."
        ),
        categories="cs.CL cs.AI cs.LG",
        primary_category="cs.CL",
        category_list=["cs.CL", "cs.AI", "cs.LG"],
        submitted_date=datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 6, 15, 8, 30, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 2),
        oai_datestamp=date(2023, 6, 15),
    ),
    sample_paper_data(
        arxiv_id="2301.00002",
        title="BERT: Pre-training of Deep Bidirectional Transformers",
        authors_text="Jacob Devlin, Ming-Wei Chang, Kenton Lee, Kristina Toutanova",
        abstract=(
            "We introduce a new language representation model called BERT, which stands "
            "for Bidirectional Encoder Representations from Transformers. BERT is designed "
            "to pre-train deep bidirectional representations by jointly conditioning on "
            "both left and right context in all layers."
        ),
        categories="cs.CL cs.LG",
        primary_category="cs.CL",
        category_list=["cs.CL", "cs.LG"],
        submitted_date=datetime(2023, 1, 2, 10, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 2, 10, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 3),
        oai_datestamp=date(2023, 1, 3),
    ),
    sample_paper_data(
        arxiv_id="2301.00003",
        title="GPT-4 Technical Report: Language Models and Reasoning",
        authors_text="OpenAI, Sam Altman, Ilya Sutskever",
        abstract=(
            "We report the development of GPT-4, a large-scale multimodal model which can "
            "accept image and text inputs and produce text outputs. GPT-4 exhibits human-level "
            "performance on various professional and academic benchmarks."
        ),
        categories="cs.CL cs.AI",
        primary_category="cs.CL",
        category_list=["cs.CL", "cs.AI"],
        submitted_date=datetime(2023, 1, 3, 14, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 3, 1, 12, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 4),
        oai_datestamp=date(2023, 3, 1),
    ),
    # cs.AI papers (Artificial Intelligence)
    sample_paper_data(
        arxiv_id="2301.00004",
        title="Reinforcement Learning from Human Feedback: A Survey",
        authors_text="Paul Christiano, Jan Leike, Dario Amodei",
        abstract=(
            "This survey examines reinforcement learning from human feedback (RLHF), "
            "a technique for aligning language models with human preferences. We discuss "
            "reward modeling, policy optimization, and the challenges of scalable oversight."
        ),
        categories="cs.AI cs.LG",
        primary_category="cs.AI",
        category_list=["cs.AI", "cs.LG"],
        submitted_date=datetime(2023, 1, 4, 8, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 4, 8, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 5),
        oai_datestamp=date(2023, 1, 5),
    ),
    sample_paper_data(
        arxiv_id="2301.00005",
        title="Neural Architecture Search: Methods and Applications",
        authors_text="Barret Zoph, Quoc V. Le",
        abstract=(
            "Neural architecture search automates the design of neural network architectures. "
            "We review search strategies including reinforcement learning, evolutionary methods, "
            "and differentiable approaches for finding optimal network structures."
        ),
        categories="cs.AI cs.LG cs.CV",
        primary_category="cs.AI",
        category_list=["cs.AI", "cs.LG", "cs.CV"],
        submitted_date=datetime(2023, 1, 5, 9, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 5, 9, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 6),
        oai_datestamp=date(2023, 1, 6),
    ),
    # stat.ML papers (Machine Learning / Statistics)
    sample_paper_data(
        arxiv_id="2301.00006",
        title="Bayesian Deep Learning: Methods and Uncertainty Estimation",
        authors_text="Yarin Gal, Zoubin Ghahramani",
        abstract=(
            "We review Bayesian approaches to deep learning, focusing on uncertainty "
            "estimation in neural networks. Bayesian methods provide principled uncertainty "
            "quantification through posterior inference over network weights."
        ),
        categories="stat.ML cs.LG",
        primary_category="stat.ML",
        category_list=["stat.ML", "cs.LG"],
        submitted_date=datetime(2023, 1, 6, 11, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 2, 1, 10, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 7),
        oai_datestamp=date(2023, 2, 1),
    ),
    sample_paper_data(
        arxiv_id="2301.00007",
        title="Random Forests and Gradient Boosting: A Unified View",
        authors_text="Leo Breiman, Jerome Friedman",
        abstract=(
            "We present a unified framework connecting random forests and gradient "
            "boosting machines. Both methods ensemble decision trees but differ in "
            "training strategy: bagging versus sequential boosting."
        ),
        categories="stat.ML",
        primary_category="stat.ML",
        category_list=["stat.ML"],
        submitted_date=datetime(2023, 1, 7, 15, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 7, 15, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 8),
        oai_datestamp=date(2023, 1, 8),
    ),
    # cs.CV papers (Computer Vision)
    sample_paper_data(
        arxiv_id="2301.00008",
        title="Vision Transformers: Attention for Image Recognition",
        authors_text="Alexei Dosovitskiy, Lucas Beyer, Alexander Kolesnikov",
        abstract=(
            "We show that a pure transformer applied directly to sequences of image "
            "patches can perform very well on image classification tasks. Vision "
            "Transformer (ViT) attains excellent results compared to state-of-the-art "
            "convolutional networks with substantially fewer computational resources."
        ),
        categories="cs.CV cs.LG",
        primary_category="cs.CV",
        category_list=["cs.CV", "cs.LG"],
        submitted_date=datetime(2023, 1, 8, 12, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 5, 1, 9, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 9),
        oai_datestamp=date(2023, 5, 1),
    ),
    sample_paper_data(
        arxiv_id="2301.00009",
        title="Diffusion Models for Image Generation",
        authors_text="Jonathan Ho, Ajay Jain, Pieter Abbeel",
        abstract=(
            "We present denoising diffusion probabilistic models, a class of latent "
            "variable models inspired by considerations from nonequilibrium thermodynamics. "
            "Our models produce high quality image synthesis results."
        ),
        categories="cs.CV cs.AI",
        primary_category="cs.CV",
        category_list=["cs.CV", "cs.AI"],
        submitted_date=datetime(2023, 1, 9, 10, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 9, 10, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 10),
        oai_datestamp=date(2023, 1, 10),
    ),
    # Recent papers (for browse_recent testing) -- announced within last 3 days of dataset
    sample_paper_data(
        arxiv_id="2301.00010",
        title="Scaling Laws for Neural Language Models",
        authors_text="Jared Kaplan, Sam McCandlish, Tom Henighan",
        abstract=(
            "We study empirical scaling laws for language model performance on the "
            "cross-entropy loss. The loss scales as a power-law with model size, "
            "dataset size, and the amount of compute used for training."
        ),
        categories="cs.CL cs.LG",
        primary_category="cs.CL",
        category_list=["cs.CL", "cs.LG"],
        submitted_date=datetime(2023, 1, 10, 14, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 10, 14, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 11),
        oai_datestamp=date(2023, 1, 11),
    ),
    sample_paper_data(
        arxiv_id="2301.00011",
        title="Constitutional AI: Harmlessness from AI Feedback",
        authors_text="Yuntao Bai, Saurav Kadavath, Amanda Askell",
        abstract=(
            "We experiment with methods for training a harmless AI assistant through "
            "self-improvement, without any human labels identifying harmful outputs. "
            "We use a set of principles to make an AI system helpful, honest, and harmless."
        ),
        categories="cs.AI cs.CL",
        primary_category="cs.AI",
        category_list=["cs.AI", "cs.CL"],
        submitted_date=datetime(2023, 1, 11, 9, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 11, 9, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 12),
        oai_datestamp=date(2023, 1, 12),
    ),
    sample_paper_data(
        arxiv_id="2301.00012",
        title="Transformer Memory and Attention Mechanisms in Machine Learning",
        authors_text="Ashish Vaswani, Noam Shazeer",
        abstract=(
            "We explore memory-augmented transformer architectures that combine attention "
            "mechanisms with external memory modules for improved long-range dependency "
            "modeling in machine learning tasks."
        ),
        categories="cs.LG cs.CL",
        primary_category="cs.LG",
        category_list=["cs.LG", "cs.CL"],
        submitted_date=datetime(2023, 1, 12, 16, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 12, 16, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 13),
        oai_datestamp=date(2023, 1, 13),
    ),
    # Papers by specific author for author search testing
    sample_paper_data(
        arxiv_id="2301.00013",
        title="Graph Neural Networks for Molecular Property Prediction",
        authors_text="Ashish Vaswani, David Duvenaud, Thomas Kipf",
        abstract=(
            "We apply graph neural networks to predict molecular properties from "
            "graph-structured molecular representations. Our approach achieves "
            "state-of-the-art results on several molecular benchmarks."
        ),
        categories="cs.LG stat.ML",
        primary_category="cs.LG",
        category_list=["cs.LG", "stat.ML"],
        submitted_date=datetime(2023, 1, 13, 8, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 13, 8, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 14),
        oai_datestamp=date(2023, 1, 14),
    ),
    # More papers for richer test coverage
    sample_paper_data(
        arxiv_id="2301.00014",
        title="Sparse Attention Patterns for Efficient Transformers",
        authors_text="Iz Beltagy, Matthew E. Peters, Arman Cohan",
        abstract=(
            "We introduce sparse attention patterns that reduce the computational "
            "complexity of transformers from quadratic to linear in sequence length. "
            "Our method achieves comparable accuracy on long document tasks."
        ),
        categories="cs.CL cs.LG",
        primary_category="cs.CL",
        category_list=["cs.CL", "cs.LG"],
        submitted_date=datetime(2023, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 14, 11, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 15),
        oai_datestamp=date(2023, 1, 15),
    ),
    sample_paper_data(
        arxiv_id="2301.00015",
        title="Protein Structure Prediction with AlphaFold",
        authors_text="John Jumper, Richard Evans, Alexander Pritzel",
        abstract=(
            "We develop AlphaFold, a system for computational protein structure "
            "prediction that achieves accuracy competitive with experimental methods. "
            "The system uses a novel neural network architecture that leverages "
            "attention over evolutionary and structural features."
        ),
        categories="cs.AI q-bio.BM",
        primary_category="cs.AI",
        category_list=["cs.AI", "q-bio.BM"],
        submitted_date=datetime(2023, 1, 15, 13, 0, 0, tzinfo=timezone.utc),
        updated_date=datetime(2023, 1, 15, 13, 0, 0, tzinfo=timezone.utc),
        announced_date=date(2023, 1, 16),
        oai_datestamp=date(2023, 1, 16),
    ),
]


@pytest.fixture
async def search_engine():
    """Create async engine for the search test database."""
    settings = get_settings()
    engine = create_async_engine(
        settings.test_database_url,
        echo=False,
        pool_pre_ping=True,
    )
    yield engine
    await engine.dispose()


@pytest.fixture
async def search_session(search_engine):
    """Create tables, populate with sample papers, yield session, then cleanup."""
    # Drop existing tables/triggers first for clean isolation
    async with search_engine.begin() as conn:
        await conn.execute(text("DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers"))
        await conn.execute(text("DROP FUNCTION IF EXISTS papers_search_vector_update()"))
        await conn.run_sync(Base.metadata.drop_all)

    async with search_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.execute(text(TSVECTOR_FUNCTION_SQL))
        await conn.execute(text(TSVECTOR_DROP_TRIGGER_SQL))
        await conn.execute(text(TSVECTOR_CREATE_TRIGGER_SQL))

    session_factory = async_sessionmaker(
        search_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with session_factory() as session:
        # Insert all sample papers
        for paper_data in SAMPLE_PAPERS:
            paper = Paper(**paper_data)
            session.add(paper)
        await session.commit()
        yield session

    async with search_engine.begin() as conn:
        await conn.execute(text("DROP TRIGGER IF EXISTS papers_search_vector_trigger ON papers"))
        await conn.execute(text("DROP FUNCTION IF EXISTS papers_search_vector_update()"))
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def search_session_factory(search_engine, search_session):
    """Return an async_sessionmaker factory for use by SearchService.

    The search_session fixture must be depended on to ensure
    tables are created and data is populated.
    """
    return async_sessionmaker(
        search_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
