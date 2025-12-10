"""initial migration

Revision ID: 4d27e8fe02e5
Revises: 94b4008a97b3
Create Date: 2025-12-08 19:04:09.211700

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '4d27e8fe02e5'
down_revision: Union[str, None] = '94b4008a97b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Division
    op.create_table(
        'Division',
        sa.Column('DivisionID', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('Name', sa.String(100), nullable=False),
    )
    op.create_index(op.f('ix_Division_DivisionID'), 'Division', ['DivisionID'], unique=False)

    # Department (references Division)
    op.create_table(
        'Department',
        sa.Column('DeptID', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('Name', sa.String(100), nullable=False),
        sa.Column('DivisionID', sa.Integer(), sa.ForeignKey('Division.DivisionID')),
    )
    op.create_index(op.f('ix_Department_DeptID'), 'Department', ['DeptID'], unique=False)

    # Employee (references Department and Division)
    op.create_table(
        'Employee',
        sa.Column('EmpID', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('Name', sa.String(100), nullable=False),
        sa.Column('Title', sa.String(100), nullable=False),
        sa.Column('DeptID', sa.Integer(), sa.ForeignKey('Department.DeptID')),
        sa.Column('DivisionID', sa.Integer(), sa.ForeignKey('Division.DivisionID')),
    )
    op.create_index(op.f('ix_Employee_EmpID'), 'Employee', ['EmpID'], unique=False)

    # Project (references Employee as Manager)
    op.create_table(
        'Project',
        sa.Column('ProjectID', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('Name', sa.String(150), nullable=False),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Budget', sa.Numeric(12, 2), nullable=True),
        sa.Column('StartDate', sa.Date(), nullable=True),
        sa.Column('EndDate', sa.Date(), nullable=True),
        sa.Column('ManagerID', sa.Integer(), sa.ForeignKey('Employee.EmpID')),
    )
    op.create_index(op.f('ix_Project_ProjectID'), 'Project', ['ProjectID'], unique=False)

    # Milestone (references Project and Employee)
    op.create_table(
        'Milestone',
        sa.Column('MilestoneID', sa.Integer(), autoincrement=True, primary_key=True),
        sa.Column('Name', sa.String(150), nullable=False),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('DueDate', sa.Date(), nullable=True),
        sa.Column('ProjectID', sa.Integer(), sa.ForeignKey('Project.ProjectID')),
        sa.Column('ResponsibleEmpID', sa.Integer(), sa.ForeignKey('Employee.EmpID')),
    )
    op.create_index(op.f('ix_Milestone_MilestoneID'), 'Milestone', ['MilestoneID'], unique=False)

    # Other alterations
    op.alter_column('JobHistory', 'Title',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('JobHistory', 'Salary',
               existing_type=mysql.DECIMAL(precision=12, scale=2),
               nullable=False)
    op.create_index(op.f('ix_Phone_PhoneNumber'), 'Phone', ['PhoneNumber'], unique=False)
    op.alter_column('ProjectHistory', 'Role',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)


def downgrade() -> None:
    # Reverse order: drop Milestone → Project → Employee → Department → Division
    op.alter_column('ProjectHistory', 'Role',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.drop_index(op.f('ix_Phone_PhoneNumber'), table_name='Phone')
    op.alter_column('JobHistory', 'Salary',
               existing_type=mysql.DECIMAL(precision=12, scale=2),
               nullable=True)
    op.alter_column('JobHistory', 'Title',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)

    op.drop_index(op.f('ix_Milestone_MilestoneID'), table_name='Milestone')
    op.drop_table('Milestone')

    op.drop_index(op.f('ix_Project_ProjectID'), table_name='Project')
    op.drop_table('Project')

    op.drop_index(op.f('ix_Employee_EmpID'), table_name='Employee')
    op.drop_table('Employee')

    op.drop_index(op.f('ix_Department_DeptID'), table_name='Department')
    op.drop_table('Department')

    op.drop_index(op.f('ix_Division_DivisionID'), table_name='Division')
    op.drop_table('Division')
    # ### end Alembic commands ###
