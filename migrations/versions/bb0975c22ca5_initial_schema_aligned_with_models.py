"""Initial schema aligned with models

Revision ID: bb0975c22ca5
Revises: 
Create Date: 2025-12-10 16:37:15.528225

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb0975c22ca5'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Building
    op.create_table(
        'Building',
        sa.Column('BuildingCode', sa.String(length=10), nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('YearBuilt', sa.Integer(), nullable=True),
        sa.Column('Cost', sa.DECIMAL(precision=12, scale=2), nullable=True),
        sa.PrimaryKeyConstraint('BuildingCode')
    )
    op.create_index(op.f('ix_Building_BuildingCode'), 'Building', ['BuildingCode'], unique=False)

    # Department (no FKs yet)
    op.create_table(
        'Department',
        sa.Column('DeptID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('Budget', sa.DECIMAL(precision=12, scale=2), nullable=True),
        sa.Column('DivisionID', sa.Integer(), nullable=True),
        sa.Column('DeptHeadID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('DeptID'),
        sa.UniqueConstraint('Name')
    )
    op.create_index(op.f('ix_Department_DeptID'), 'Department', ['DeptID'], unique=False)

    # Division (no FKs yet)
    op.create_table(
        'Division',
        sa.Column('DivisionID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('DivHeadID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('DivisionID')
    )
    op.create_index(op.f('ix_Division_DivisionID'), 'Division', ['DivisionID'], unique=False)

    # Employee (no FKs yet)
    op.create_table(
        'Employee',
        sa.Column('EmpID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('Name', sa.String(length=100), nullable=False),
        sa.Column('Title', sa.String(length=100), nullable=True),
        sa.Column('OfficeID', sa.Integer(), nullable=True),
        sa.Column('DeptID', sa.Integer(), nullable=True),
        sa.Column('DivisionID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('EmpID')
    )
    op.create_index(op.f('ix_Employee_EmpID'), 'Employee', ['EmpID'], unique=False)

    # Office
    op.create_table(
        'Office',
        sa.Column('OfficeID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('AreaSqFt', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('OfficeID')
    )

    # JobHistory
    op.create_table(
        'JobHistory',
        sa.Column('EmpID', sa.Integer(), nullable=False),
        sa.Column('StartDate', sa.Date(), nullable=False),
        sa.Column('Title', sa.String(length=100), nullable=False),
        sa.Column('Salary', sa.DECIMAL(precision=12, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('EmpID', 'StartDate')
    )

    # Phone
    op.create_table(
        'Phone',
        sa.Column('PhoneNumber', sa.String(length=15), nullable=False),
        sa.Column('OfficeID', sa.Integer(), nullable=True),
        sa.Column('EmpID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('PhoneNumber')
    )
    op.create_index(op.f('ix_Phone_PhoneNumber'), 'Phone', ['PhoneNumber'], unique=False)

    # Project
    op.create_table(
        'Project',
        sa.Column('ProjectID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('Name', sa.String(length=150), nullable=False),
        sa.Column('Description', sa.Text(), nullable=True),
        sa.Column('Budget', sa.DECIMAL(precision=12, scale=2), nullable=True),
        sa.Column('StartDate', sa.Date(), nullable=True),
        sa.Column('EndDate', sa.Date(), nullable=True),
        sa.Column('ManagerID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('ProjectID')
    )
    op.create_index(op.f('ix_Project_ProjectID'), 'Project', ['ProjectID'], unique=False)

    # Room
    op.create_table(
        'Room',
        sa.Column('BuildingCode', sa.String(length=10), nullable=False),
        sa.Column('RoomNumber', sa.Integer(), nullable=False),
        sa.Column('RoomType', sa.String(length=50), nullable=True),
        sa.PrimaryKeyConstraint('BuildingCode', 'RoomNumber')
    )

    # TaxReports
    op.create_table(
        'tax_reports',
        sa.Column('ReportID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('EmpID', sa.Integer(), nullable=False),
        sa.Column('Year', sa.Integer(), nullable=False),
        sa.Column('FederalTax', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('StateTax', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('OtherTax', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.PrimaryKeyConstraint('ReportID')
    )

    # Milestone
    op.create_table(
        'Milestone',
        sa.Column('MilestoneID', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('Description', sa.Text(), nullable=False),
        sa.Column('Status', sa.String(length=50), nullable=False),
        sa.Column('DueDate', sa.Date(), nullable=True),
        sa.Column('ProjectID', sa.Integer(), nullable=True),
        sa.Column('ResponsibleEmpID', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('MilestoneID')
    )
    op.create_index(op.f('ix_Milestone_MilestoneID'), 'Milestone', ['MilestoneID'], unique=False)

    # ProjectHistory
    op.create_table(
        'ProjectHistory',
        sa.Column('EmpID', sa.Integer(), nullable=False),
        sa.Column('ProjectID', sa.Integer(), nullable=False),
        sa.Column('Role', sa.String(length=100), nullable=False),
        sa.Column('TimeSpent', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('EmpID', 'ProjectID')
    )

    # Now add foreign keys after all tables exist
    op.create_foreign_key('fk_department_division', 'Department', 'Division', ['DivisionID'], ['DivisionID'])
    op.create_foreign_key('fk_department_employee', 'Department', 'Employee', ['DeptHeadID'], ['EmpID'])
    op.create_foreign_key('fk_division_employee', 'Division', 'Employee', ['DivHeadID'], ['EmpID'])
    op.create_foreign_key('fk_employee_department', 'Employee', 'Department', ['DeptID'], ['DeptID'])
    op.create_foreign_key('fk_employee_division', 'Employee', 'Division', ['DivisionID'], ['DivisionID'])
    op.create_foreign_key('fk_employee_office', 'Employee', 'Office', ['OfficeID'], ['OfficeID'])
    op.create_foreign_key('fk_jobhistory_employee', 'JobHistory', 'Employee', ['EmpID'], ['EmpID'])
    op.create_foreign_key('fk_phone_employee', 'Phone', 'Employee', ['EmpID'], ['EmpID'])
    op.create_foreign_key('fk_phone_office', 'Phone', 'Office', ['OfficeID'], ['OfficeID'])
    op.create_foreign_key('fk_project_employee', 'Project', 'Employee', ['ManagerID'], ['EmpID'])
    op.create_foreign_key('fk_room_building', 'Room', 'Building', ['BuildingCode'], ['BuildingCode'])
    op.create_foreign_key('fk_taxreports_employee', 'tax_reports', 'Employee', ['EmpID'], ['EmpID'])
    op.create_foreign_key('fk_milestone_project', 'Milestone', 'Project', ['ProjectID'], ['ProjectID'])
    op.create_foreign_key('fk_milestone_employee', 'Milestone', 'Employee', ['ResponsibleEmpID'], ['EmpID'])
    op.create_foreign_key('fk_projecthistory_employee', 'ProjectHistory', 'Employee', ['EmpID'], ['EmpID'])
    op.create_foreign_key('fk_projecthistory_project', 'ProjectHistory', 'Project', ['ProjectID'], ['ProjectID'])


def downgrade() -> None:
    # Drop foreign keys first
    op.drop_constraint('fk_projecthistory_project', 'ProjectHistory', type_='foreignkey')
    op.drop_constraint('fk_projecthistory_employee', 'ProjectHistory', type_='foreignkey')
    op.drop_table('ProjectHistory')

    op.drop_index(op.f('ix_Milestone_MilestoneID'), table_name='Milestone')
   
    # ### end Alembic commands ###
